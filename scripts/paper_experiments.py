#!/usr/bin/env python3
"""Execute original paper artifacts, preserving provenance and the actual scope."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
COVERUP_EVAL_REVISION = "f3173196b90181974b0b684600ffde42ac36672c"


def save(out, command, cwd, scope, env=None, source=None):
    if out.exists():
        raise ValueError("Output exists; choose a fresh directory")
    out.mkdir(parents=True)
    started = datetime.now(timezone.utc).isoformat()
    result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True)
    clean = lambda s: s.replace(str(ROOT), "<repo>").replace(str(cwd), "<artifact>").replace(str(Path.home()), "<home>")
    output = clean(result.stdout+result.stderr)
    (out/"output.log").write_text(output)
    meta = {"started_at_utc": started, "finished_at_utc": datetime.now(timezone.utc).isoformat(),
            "command": [clean(str(c)) for c in command], "exit_code": result.returncode, "scope": scope,
            "new_model_generation": False, "source": source or {}}
    if scope == "published-data-reanalysis" and result.returncode == 0:
        matches = re.findall(r"'([^']+)': (\[[^\n]+\])", result.stdout)
        meta["metrics"] = {name: json.loads(values) for name, values in matches}
        meta["metric_order"] = ["overall_line", "overall_branch", "overall_line_branch", "median_module_line", "median_module_branch", "median_module_line_branch"]
    (out/"run.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps(meta, ensure_ascii=False, indent=2))
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)
    replay = sub.add_parser("coverup-reanalyse")
    replay.add_argument("artifact", type=Path)
    replay.add_argument("--python", default=sys.executable)
    replay.add_argument("--output", type=Path, required=True)
    dry = sub.add_parser("coverup-dry-run")
    dry.add_argument("--python", required=True)
    dry.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.mode == "coverup-reanalyse":
            artifact = args.artifact.resolve()
            revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=artifact, text=True).strip()
            if revision != COVERUP_EVAL_REVISION:
                raise ValueError("Use the pinned artifact revision in research/papers.json")
            # macOS may report an unrelated case-colliding CM filename as dirty.
            # Check exactly the analysis script and MT inputs used by this run.
            subprocess.run(["git", "diff", "--exit-code", "HEAD", "--", "scripts/compare.py", "MuTAP-benchmarks", "MuTAP-results", "output/mutap.gpt4o-v2"], cwd=artifact, check=True, stdout=subprocess.DEVNULL)
            script = artifact/"scripts/compare.py"
            return save(args.output, [args.python, "scripts/compare.py", "--suite", "mutap", "--to", "mutap-gpt4o_zero", "--array"], artifact,
                        "published-data-reanalysis", source={"url": "https://github.com/plasma-umass/coverup-eval", "revision": revision,
                        "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
                        "limitation": "Original author data and script; no fresh LLM calls or fresh benchmark test execution. Analysis dependencies differ from original pins; record your environment."})
        if args.mode == "coverup-dry-run":
            # Disposable snapshot: original tool may create logs/checkpoints/tests.
            out = args.output.resolve()
            if out.exists():
                raise ValueError("Output exists")
            work = Path(tempfile.mkdtemp(prefix="seminar-coverup-"))
            (work/"scripts").mkdir()
            (work/"tests").mkdir()
            shutil.copy2(ROOT/"scripts/coverage_gaps.py", work/"scripts/coverage_gaps.py")
            (work/"tests/test_smoke.py").write_text("from pathlib import Path\nfrom scripts.coverage_gaps import extract\ndef test_empty_report(tmp_path):\n    xml = tmp_path/'jacoco.xml'\n    xml.write_text('<report/>')\n    assert extract(xml)['gaps'] == []\n")
            env = dict(os.environ)
            # Upstream validates presence even in dry-run. This sentinel is not a credential.
            env["OPENAI_API_KEY"] = "dry-run-sentinel-no-api-call"
            result = save(out, [args.python, "-m", "coverup", "--model", "gpt-4o", "--dry-run", "--tests-dir", "tests", "--package-dir", "scripts", "--no-checkpoint", "scripts/coverage_gaps.py"], work,
                        "group-source-dry-run-no-generation", env=env,
                        source={"tool": "CoverUp 0.6.0", "target": "scripts/coverage_gaps.py", "target_sha256": hashlib.sha256((work/"scripts/coverage_gaps.py").read_bytes()).hexdigest()})
            shutil.copytree(work/"tests", out/"inputs", ignore=shutil.ignore_patterns("__pycache__"))
            shutil.rmtree(work)
            return result
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    sys.exit(main())
