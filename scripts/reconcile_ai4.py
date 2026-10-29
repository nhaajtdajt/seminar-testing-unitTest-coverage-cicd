#!/usr/bin/env python3
"""Recompute an AI-4 report from saved CSV/XML, without calling Gemini or running Java."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import shutil
import sys

import ai_csv
import gemini_client as client


def without_normalization(schema):
    result = deepcopy(schema)
    for column in result["columns"]:
        column.pop("normalization", None)
    return result


def reconcile_saved(run, output, comparison_schema=None, notes=None, update=False):
    run, output = run.resolve(), output.resolve()
    if update and not output.is_relative_to(run):
        raise ValueError("Updating canonical reports requires an archive directory inside the run")
    original = json.loads((run / "schema.json").read_text())
    previous_revision = run / "report-revision.json"
    if comparison_schema is None and previous_revision.exists():
        revision = json.loads(previous_revision.read_text())
        comparison_schema = (run / revision["comparison_schema"]).resolve()
        if not comparison_schema.is_relative_to(run):
            raise ValueError("Reviewed comparison schema must stay inside the saved run")
        prior_notes = comparison_schema.parent / "review-notes.md"
        if notes is None and prior_notes.is_file():
            notes = prior_notes
    schema = json.loads(comparison_schema.read_text()) if comparison_schema else original
    ai_csv.validate_schema(original)
    ai_csv.validate_schema(schema)
    if without_normalization(schema) != without_normalization(original):
        raise ValueError("Reviewed schema may only add/change normalization; preserve original types/roles/header/harness")
    human, ai = run / "inputs/human/cases.csv", run / "generated/cases.csv"
    ai_csv.check_frozen(run / "inputs/human", schema["target_class"])
    harness = run / "generated" / schema["harness_file"]
    if ai_csv.digest(harness) != schema["harness_sha256"]:
        raise ValueError("Executed harness differs from saved schema")
    output.mkdir(parents=True, exist_ok=False)
    # Archive the earlier derived view; model responses/CSV/Java/XML are untouched.
    for name in ("comparison.json", "reconciliation.json", "report.md", "report-revision.json"):
        if (run / name).exists():
            (output / "previous").mkdir(exist_ok=True)
            shutil.copy2(run / name, output / "previous" / name)
    comparison = ai_csv.compare(human, ai, schema)
    result = ai_csv.reconcile(run, schema["target_class"], human, ai, schema, comparison, harness)
    text = ai_csv.report(result)
    if notes:
        (output / "review-notes.md").write_text(notes.read_text())
        text += "\n## Ghi chú review sau lượt chạy\n\n" + notes.read_text().strip() + "\n"
    client.save(output / "schema.json", schema)
    client.save(output / "comparison.json", comparison)
    client.save(output / "reconciliation.json", result)
    metadata = {"processed_at_utc": client.utc(), "operation": "offline report correction",
                "api_called": False, "java_rerun": False, "raw_artifacts_modified": False,
                "consistent": result["consistent"], "human_sha256": ai_csv.digest(human),
                "ai_sha256": ai_csv.digest(ai), "harness_sha256": ai_csv.digest(harness)}
    client.save(output / "revision.json", metadata)
    (output / "report.md").write_text(text)
    if update:
        relative = output.relative_to(run).as_posix()
        text += f"\nBản đối chiếu sửa offline: [{relative}/revision.json]({relative}/revision.json). "
        text += f"Schema so sánh có chuẩn hóa: [{relative}/schema.json]({relative}/schema.json). "
        text += "Không gọi lại model hoặc chạy lại Java; bản báo cáo trước nằm trong `previous/` của thư mục revision.\n"
        for name in ("comparison.json", "reconciliation.json"):
            shutil.copy2(output / name, run / name)
        (run / "report.md").write_text(text)
        client.save(run / "report-revision.json", {**metadata, "revision_directory": relative,
                    "comparison_schema": relative + "/schema.json"})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path, help="Fresh archive directory")
    parser.add_argument("--comparison-schema", type=Path)
    parser.add_argument("--notes", type=Path)
    parser.add_argument("--update-reports", action="store_true")
    args = parser.parse_args()
    try:
        result = reconcile_saved(args.run.resolve(), args.output.resolve(), args.comparison_schema,
                                 args.notes, args.update_reports)
        print(json.dumps({"consistent": result["consistent"],
            "matching_inputs": result["comparison"]["matching_inputs"],
            "matching_outcomes": result["comparison"]["matching_outcomes"],
            "disagreements": len(result["comparison"]["disagreements"]),
            "representation_differences": len(result["comparison"]["representation_differences"])}, indent=2))
        return 0 if result["consistent"] else 1
    except (ValueError, OSError, KeyError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    sys.exit(main())
