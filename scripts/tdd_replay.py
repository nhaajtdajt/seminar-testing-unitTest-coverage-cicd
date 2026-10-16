#!/usr/bin/env python3
"""Replay four real red/green test cycles in an isolated copy; never fabricates past commits."""
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "evidence/tuan-05/tdd-replay"

def main():
    if DEST.exists():
        raise SystemExit("Evidence exists; move it aside explicitly before replaying")
    DEST.mkdir(parents=True)
    outcomes = []
    implementations = [
        'throw new UnsupportedOperationException("Chưa cài đặt");',
        'return BigDecimal.ZERO;',
        'return BigDecimal.valueOf(daysLate * 2000L);',
        'return BigDecimal.valueOf(tier == MemberTier.VIP ? Math.max(0, daysLate - 2L) * 1000 : daysLate * 2000L);',
        'return BigDecimal.valueOf(Math.min(50000L, tier == MemberTier.VIP ? Math.max(0, daysLate - 2L) * 1000 : daysLate * 2000L));'
    ]
    cases = [(0, 'NORMAL', '0'), (3, 'NORMAL', '6000'), (3, 'VIP', '1000'), (40, 'NORMAL', '50000')]
    with tempfile.TemporaryDirectory(prefix="seminar-tdd-") as temporary:
        project = Path(temporary) / "case-study"
        shutil.copytree(ROOT / "case-study", project, ignore=shutil.ignore_patterns("target"))
        source = project / "src/main/java/vn/edu/seminar/fine/FineCalculator.java"
        test = project / "src/test/java/vn/edu/seminar/fine/TddRoundTest.java"
        for round_number in range(1, 5):
            methods = '\n'.join(f'@Test void case{i}() {{ assertThat(new FineCalculator().calculate({days}, MemberTier.{tier})).isEqualByComparingTo("{amount}"); }}' for i, (days, tier, amount) in enumerate(cases[:round_number]))
            test.write_text('package vn.edu.seminar.fine;\nimport org.junit.jupiter.api.Test;\nimport static org.assertj.core.api.Assertions.assertThat;\nclass TddRoundTest {\n'+methods+'\n}\n')
            for state, implementation in [('red', implementations[round_number-1]), ('green', implementations[round_number])]:
                source.write_text('package vn.edu.seminar.fine;\nimport java.math.BigDecimal;\npublic final class FineCalculator { public BigDecimal calculate(int daysLate, MemberTier tier) { '+implementation+' } }\n')
                label = f"round-{round_number}-{state}"
                snapshot = DEST / label
                snapshot.mkdir()
                shutil.copy2(source, snapshot / "FineCalculator.java")
                shutil.copy2(test, snapshot / "TddRoundTest.java")
                command = [str(project/'mvnw'), '-B', '-ntp', '-f', str(project/'pom.xml'), '-Dtest=TddRoundTest', '-Dtest.excludedTags=', 'clean', 'test']
                start = datetime.now(timezone.utc).isoformat()
                timer = time.monotonic()
                with (snapshot / "output.log").open('w') as log:
                    result = subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
                entry = {"round": round_number, "state": state, "started_at_utc": start, "exit_code": result.returncode, "seconds": round(time.monotonic()-timer, 3), "command": command}
                outcomes.append(entry)
                (snapshot / "run.json").write_text(json.dumps(entry, indent=2)+"\n")
                print(f"{label}: exit={result.returncode}", flush=True)
                surefire = project / "target/surefire-reports/TEST-vn.edu.seminar.fine.TddRoundTest.xml"
                if not surefire.exists():
                    raise RuntimeError(f"{label}: no Surefire report, failure may not be a test failure")
                shutil.copy2(surefire, snapshot / "surefire.xml")
                if (state == 'red' and result.returncode == 0) or (state == 'green' and result.returncode != 0):
                    raise RuntimeError(f"Unexpected TDD outcome: {label}")
    (DEST / "summary.json").write_text(json.dumps({"provenance": "Educational replay executed now, not historical team work or commit history", "rounds": outcomes}, indent=2)+"\n")

if __name__ == "__main__":
    main()
