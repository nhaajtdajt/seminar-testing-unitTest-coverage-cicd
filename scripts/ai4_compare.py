#!/usr/bin/env python3
"""Freeze a human-authored oracle before comparing it with AI output."""
import argparse
import csv
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import io
import json
from pathlib import Path

FIELDS = ["daysLate", "tier", "expected", "expectedException"]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_cases(data, ai=False):
    reader = csv.DictReader(io.StringIO(data.decode("utf-8-sig")))
    allowed_headers = [FIELDS[:3], FIELDS] if ai else [FIELDS]
    if reader.fieldnames not in allowed_headers:
        raise ValueError("Unexpected CSV header")
    cases = {}
    for row in reader:
        if None in row or any(v is None for v in row.values()):
            raise ValueError("Malformed CSV row")
        days = int(row["daysLate"])
        if not -(2**31) <= days < 2**31 or row["tier"] not in {"NORMAL", "VIP", "NULL"}:
            raise ValueError("Invalid Java int or tier")
        key = (days, row["tier"])
        if key in cases:
            raise ValueError(f"Duplicate input: {key}")
        error = row.get("expectedException", "")
        if error:
            if error != "IllegalArgumentException" or row["expected"]:
                raise ValueError("Use a blank amount with IllegalArgumentException")
            outcome = error
        else:
            try:
                amount = Decimal(row["expected"])
            except InvalidOperation as exc:
                raise ValueError("Invalid expected amount") from exc
            if not amount.is_finite() or amount < 0:
                raise ValueError("Expected amount must be finite and nonnegative")
            outcome = format(amount.normalize(), "f")
        cases[key] = outcome
    if not cases:
        raise ValueError("Human must supply cases; an empty template is not an oracle")
    return cases


def freeze(source, destination, author):
    data = source.read_bytes()
    cases = read_cases(data)
    if not author.strip() or not any(v == "IllegalArgumentException" for v in cases.values()):
        raise ValueError("Supply the real author and at least one invalid-input case")
    if all(v == "IllegalArgumentException" for v in cases.values()):
        raise ValueError("Supply at least one valid-input case")
    destination.mkdir(parents=True, exist_ok=False)
    (destination / "cases.csv").write_bytes(data)
    receipt = {"author": author, "frozen_at_utc": datetime.now(timezone.utc).isoformat(),
               "sha256": digest(data), "case_count": len(cases),
               "attestation": "Author states these cases were written without viewing AI output or reference test data.",
               "limitation": "Self-attestation and hash preserve provenance; they cannot prove human independence."}
    (destination / "receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+"\n")
    return receipt


def compare(frozen, ai_path):
    data = (frozen / "cases.csv").read_bytes()
    receipt = json.loads((frozen / "receipt.json").read_text())
    if digest(data) != receipt["sha256"]:
        raise ValueError("Frozen oracle changed; comparison refused")
    human = read_cases(data)
    ai = read_cases(ai_path.read_bytes(), ai=True)
    shared = human.keys() & ai.keys()
    encode = lambda key: {"daysLate": key[0], "tier": key[1]}
    return {"human_sha256": receipt["sha256"], "ai_sha256": digest(ai_path.read_bytes()),
            "human_cases": len(human), "ai_cases": len(ai),
            "matching_inputs": len(shared),
            "matching_outcomes": sum(human[k] == ai[k] for k in shared),
            "disagreements": [{**encode(k), "human": human[k], "ai": ai[k]} for k in sorted(shared) if human[k] != ai[k]],
            "missing_from_ai": [encode(k) for k in sorted(human.keys()-ai.keys())],
            "extra_in_ai": [encode(k) for k in sorted(ai.keys()-human.keys())],
            "limitation": "Agreement with the human oracle is not proof of correctness; run both against Java and review the specification."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    lock = sub.add_parser("freeze")
    lock.add_argument("source", type=Path)
    lock.add_argument("destination", type=Path)
    lock.add_argument("--author", required=True)
    lock.add_argument("--attest-independent", action="store_true", required=True)
    diff = sub.add_parser("compare")
    diff.add_argument("frozen", type=Path)
    diff.add_argument("ai", type=Path)
    diff.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.action == "freeze":
            result = freeze(args.source, args.destination, args.author)
        else:
            result = compare(args.frozen, args.ai)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(1, f"{exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
