#!/usr/bin/env python3
"""Measure three local cold/warm Maven pairs or JaCoCo off/on pairs; never labels them CI runs."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import signal
import statistics
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]

def save_summary(dest, mode, entries):
    modes = ['cold', 'warm'] if mode == 'cache' else ['off', 'on']
    completed = [trial for trial in range(1, 4) if all(
        any(e['trial'] == trial and e['mode'] == label and e['exit_code'] == 0 for e in entries)
        for label in modes)]
    valid = [e for e in entries if e['trial'] in completed]
    summary = {
        'environment': 'Local JVM; not GitHub cache, Actions timing or Jenkins execution',
        'complete': len(completed) == 3, 'planned_pairs': 3, 'completed_pairs': len(completed),
        'medians_seconds': {label: statistics.median(e['seconds'] for e in valid if e['mode'] == label)
                            for label in modes} if valid else {},
        'measurements': entries,
        'note': 'Completed pairs only. Previous failed/interrupted attempts are retained in failed-attempts/. Resumed pairs can be executed later; see per-run timestamps and commands.'}
    (dest / 'summary.json').write_text(json.dumps(summary, indent=2)+'\n')

def run_timed(command, log_path, timeout_seconds):
    start = datetime.now(timezone.utc).isoformat()
    timer = time.monotonic()
    with log_path.open('x') as log:
        process = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                                   start_new_session=True)
        timed_out = False
        try:
            code = process.wait(timeout=timeout_seconds)
        except (subprocess.TimeoutExpired, KeyboardInterrupt) as error:
            timed_out = isinstance(error, subprocess.TimeoutExpired)
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            code = 124 if timed_out else 130
            log.write(f'\nBenchmark stopped: {"time limit exceeded" if timed_out else "interrupted"}.\n')
    return {'started_at_utc': start, 'finished_at_utc': datetime.now(timezone.utc).isoformat(),
            'seconds': round(time.monotonic()-timer, 3), 'exit_code': code,
            'command': command, 'timed_out': timed_out, 'time_limit_seconds': timeout_seconds}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["cache", "jacoco"])
    parser.add_argument('--resume', action='store_true', help='Keep completed pairs and run missing pairs only')
    parser.add_argument('--timeout-seconds', type=int, default=180, help='Time limit per Maven invocation')
    parser.add_argument('--request-timeout-seconds', type=int, default=30, help='Maven HTTP inactivity timeout')
    args = parser.parse_args()
    if args.timeout_seconds <= 0:
        parser.error('Time limit must be positive')
    if args.request_timeout_seconds <= 0:
        parser.error('Request timeout must be positive')
    dest = ROOT / "evidence/tuan-05" / f"benchmark-{args.mode}"
    if dest.exists() and not args.resume:
        parser.error("Evidence directory already exists; preserve it and use a fresh copy to rerun")
    dest.mkdir(parents=True, exist_ok=args.resume)
    measurements = dest / 'measurements.json'
    entries = json.loads(measurements.read_text()) if args.resume and measurements.exists() else []
    modes = ['cold', 'warm'] if args.mode == 'cache' else ['off', 'on']
    for trial in {e['trial'] for e in entries}:
        selected = [e for e in entries if e['trial'] == trial]
        if len(selected) != 2 or {e['mode'] for e in selected} != set(modes) or any(e['exit_code'] != 0 for e in selected):
            parser.error('Only complete successful pairs can be resumed; preserve partial evidence separately')
    completed = {e['trial'] for e in entries}
    remaining = [trial for trial in range(1, 4) if trial not in completed]
    if not remaining:
        print('Already complete: 3/3 pairs. No measurements were overwritten.')
        return
    with tempfile.TemporaryDirectory(prefix="seminar-benchmark-") as temporary:
        project = Path(temporary) / "case-study"
        shutil.copytree(ROOT / "case-study", project, ignore=shutil.ignore_patterns("target"))
        environment = subprocess.run([str(project/'mvnw'), '-v'], capture_output=True, text=True, timeout=30)
        if environment.returncode:
            raise RuntimeError('Maven Wrapper environment check failed')
        for trial in remaining:
            (dest / f'{trial}-environment.txt').write_text(environment.stdout+environment.stderr)
            pair = []
            pair_logs = []
            modes = ['cold', 'warm'] if args.mode == 'cache' else (['off', 'on'] if trial % 2 else ['on', 'off'])
            for mode in modes:
                command = [str(project / 'mvnw'), '-B', '-ntp', '-f', str(project / 'pom.xml')]
                # Maven 3.9.16 ships Resolver 1.9.x, which uses the connector.* keys.
                command += ['-Daether.connector.connectTimeout=15000',
                            f'-Daether.connector.requestTimeout={args.request_timeout_seconds * 1000}']
                if args.mode == 'cache':
                    command.append(f'-Dmaven.repo.local={temporary}/repo-{trial}')
                    if mode == 'cold' and Path(temporary, f'repo-{trial}').exists():
                        raise RuntimeError('Cold run repository must be empty')
                elif mode == 'off':
                    command.append('-Djacoco.skip=true')
                command += ['clean', 'verify']
                log_path = dest / f'{trial}-{mode}.log'
                if log_path.exists():
                    raise RuntimeError(f'Refusing to overwrite existing log: {log_path}')
                print(f'Starting {trial}-{mode}; time limit {args.timeout_seconds}s', flush=True)
                entry = run_timed(command, log_path, args.timeout_seconds)
                entry.update(trial=trial, mode=mode)
                entry['java_home'] = os.environ.get('JAVA_HOME')
                entry['ipv4_preferred'] = '-Djava.net.preferIPv4Stack=true' in os.environ.get('MAVEN_OPTS', '').split()
                pair.append(entry)
                pair_logs.append(log_path)
                print(f'{trial}-{mode}: {entry["seconds"]}s, exit={entry["exit_code"]}', flush=True)
                if entry['exit_code']:
                    attempt = dest/'failed-attempts'/datetime.now(timezone.utc).strftime('retry-%Y%m%dT%H%M%S%f')
                    attempt.mkdir(parents=True)
                    for log in pair_logs:
                        shutil.move(str(log), str(attempt/log.name))
                    (attempt/'measurements.json').write_text(json.dumps(pair, indent=2)+'\n')
                    save_summary(dest, args.mode, entries)
                    raise RuntimeError(f'Pair failed; evidence saved in {attempt}. Completed pairs preserved.')
            entries.extend(pair)
            measurements.write_text(json.dumps(entries, indent=2)+'\n')
            save_summary(dest, args.mode, entries)
    print(f'Complete: {len(entries)//2}/3 successful pairs.', flush=True)

if __name__ == '__main__':
    main()
