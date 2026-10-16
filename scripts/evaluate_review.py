#!/usr/bin/env python3
"""Compare a review against a seeded fixture. Exact file/rule and +/-2 lines are required."""
import argparse
import json
from pathlib import Path

def evaluate(expected, actual):
    unmatched = list(expected["findings"])
    true_positive, false_positive = [], []
    for item in actual["findings"]:
        found = next((e for e in unmatched if e["file"] == item["file"] and e["rule"] == item["rule"] and abs(e["line"]-item["line"]) <= 2), None)
        if found is None:
            false_positive.append(item)
        else:
            unmatched.remove(found)
            true_positive.append(item)
    return {"true_positive": len(true_positive), "false_positive": len(false_positive), "false_negative": len(unmatched),
            "missed": unmatched, "extra": false_positive,
            "limitation": "Seeded fixture only; same-session AI fixture/review is not an independent benchmark."}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("expected", type=Path)
    parser.add_argument("actual", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evaluate(json.loads(args.expected.read_text()), json.loads(args.actual.read_text())), ensure_ascii=False, indent=2)+"\n")
