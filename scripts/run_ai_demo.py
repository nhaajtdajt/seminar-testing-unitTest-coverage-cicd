#!/usr/bin/env python3
"""Run isolated AI demo profiles and retain portable, current evidence."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PROFILES = {"draft": "ai-loan-draft", "improved": "ai-loan-improved", "mistake": "ai-loan-mistake",
            "human": "ai-human", "data": "ai-data"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", choices=[*PROFILES, "full", "mutation"])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    dataset = None
    if args.scenario in ("human", "data"):
        relative = "ai/human/frozen/cases.csv" if args.scenario == "human" else "ai/data/AI-4-boundaries.csv"
        digest = hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()
        if args.scenario == "human":
            receipt = json.loads((ROOT/"ai/human/frozen/receipt.json").read_text())
            if digest != receipt["sha256"]:
                parser.error("Frozen human data changed; execution refused")
        dataset = {"path": relative, "sha256": digest,
                   "origin": "user-supplied data; independence declared in supplied notes" if args.scenario == "human" else "existing AI-generated CSV"}
    if args.output.exists():
        parser.error("Output exists; use a new directory to retain previous evidence")
    args.output.mkdir(parents=True)
    command = ["case-study/mvnw", "-B", "-ntp", "-f", "case-study/pom.xml"]
    if args.scenario in PROFILES:
        command += ["-P"+PROFILES[args.scenario]]
    if args.scenario == "mutation":
        command += ["-Pai-loan-improved", "clean", "test-compile", "org.pitest:pitest-maven:mutationCoverage"]
    else:
        command += ["clean", "verify"]
    started = datetime.now(timezone.utc).isoformat()
    started_epoch = time.time()
    clock = time.monotonic()
    result = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    def portable(text):
        return text.replace(str(ROOT), "<repo>").replace(str(Path.home()), "<home>")
    (args.output/"output.log").write_text(portable(result.stdout))
    metadata = {"scenario": args.scenario, "command": command, "started_at_utc": started,
                "finished_at_utc": datetime.now(timezone.utc).isoformat(),
                "elapsed_seconds": round(time.monotonic()-clock, 3), "exit_code": result.returncode,
                "expected_exit_code": 1 if args.scenario == "mistake" else 0,
                "environment": "local execution by Codex; not a paper reproduction or a user self-run",
                "java": subprocess.run(["java", "-version"], capture_output=True, text=True).stderr.strip(),
                "test_summaries": []}
    if dataset:
        metadata["dataset"] = dataset
    for path in sorted((ROOT/"case-study/target/surefire-reports").glob("TEST-*.xml")):
        if path.stat().st_mtime < started_epoch:
            continue
        suite = ET.parse(path).getroot()
        metadata["test_summaries"].append({k: suite.get(k) for k in ["name", "tests", "failures", "errors", "skipped"]})
    jacoco = ROOT/"case-study/target/site/jacoco/jacoco.xml"
    if jacoco.exists() and jacoco.stat().st_mtime >= started_epoch:
        report_directory = args.output/"site/jacoco"
        report_directory.mkdir(parents=True)
        shutil.copy2(jacoco, report_directory/"jacoco.xml")
        report = ET.parse(jacoco).getroot()
        target_name = "vn/edu/seminar/fine/FineCalculator" if dataset else "vn/edu/seminar/loan/LoanService"
        target = report.find(f".//class[@name='{target_name}']")
        metadata["fine_coverage" if dataset else "loan_coverage"] = {c.get("type"): {"covered": int(c.get("covered")), "missed": int(c.get("missed"))} for c in target.findall("counter")}
    mutations = ROOT/"case-study/target/pit-reports/mutations.xml"
    if mutations.exists() and mutations.stat().st_mtime >= started_epoch:
        report_directory = args.output/"pit-reports"
        report_directory.mkdir(parents=True)
        (report_directory/"mutations.xml").write_text(portable(mutations.read_text()))
        statuses = {}
        for mutation in ET.parse(mutations).getroot():
            status = mutation.get("status")
            statuses[status] = statuses.get(status, 0)+1
        metadata["mutations"] = statuses
    (args.output/"run.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps(metadata, ensure_ascii=False, indent=2))
    expected = metadata["expected_exit_code"]
    if result.returncode != expected:
        return 1
    if args.scenario == "mistake":
        suites = metadata["test_summaries"]
        # A dependency/build failure is not evidence of the seeded wrong oracle.
        if not any(s["name"].endswith("LoanServiceAiMistakeTest") and s["failures"] == "1" and s["errors"] == "0" for s in suites):
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
