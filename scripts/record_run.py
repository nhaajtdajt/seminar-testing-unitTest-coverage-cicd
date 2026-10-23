#!/usr/bin/env python3
"""Run a command and retain its actual command, timestamps, exit code and test reports."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name")
    parser.add_argument("--expect", type=int, default=0)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command or Path(args.name).name != args.name:
        parser.error("Provide a plain run name and a command after --")
    destination = ROOT / "evidence/tuan-06" / args.name
    if destination.exists():
        parser.error(f"Run already exists: {destination}; use a new name to preserve evidence")
    destination.mkdir(parents=True)
    started_epoch = time.time()
    start = datetime.now(timezone.utc).isoformat()
    clock = time.monotonic()
    with (destination / "output.log").open("w", encoding="utf-8") as log:
        result = subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
    metadata = {"started_at_utc": start, "finished_at_utc": datetime.now(timezone.utc).isoformat(),
                "elapsed_seconds": round(time.monotonic()-clock, 3), "command": command,
                "exit_code": result.returncode, "expected_exit_code": args.expect,
                "environment": "local; not a GitHub Actions or Jenkins execution"}
    (destination / "run.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2)+"\n")
    for relative in ["site/jacoco", "surefire-reports", "pit-reports"]:
        source = ROOT / "case-study/target" / relative
        # Do not attach Java reports left over from an earlier unrelated command.
        fresh = source.exists() and any(p.is_file() and p.stat().st_mtime >= started_epoch for p in source.rglob('*'))
        if fresh:
            shutil.copytree(source, destination / relative, dirs_exist_ok=True)
    print(json.dumps(metadata, ensure_ascii=False))
    print("\n".join((destination / "output.log").read_text(errors="replace").splitlines()[-18:]))
    return 0 if result.returncode == args.expect else 1

if __name__ == "__main__":
    sys.exit(main())
