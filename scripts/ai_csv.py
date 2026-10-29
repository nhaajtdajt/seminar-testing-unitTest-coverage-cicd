"""Schema-driven CSV validation, independent comparison and report reconciliation."""
import csv
from decimal import Decimal, InvalidOperation
import hashlib
import io
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_schema(value, header=None):
    if not isinstance(value, dict):
        raise ValueError("Schema must be a JSON object")
    columns = value.get("columns")
    if not isinstance(columns, list) or not columns:
        raise ValueError("Schema must define columns")
    names = []
    for column in columns:
        if not isinstance(column, dict):
            raise ValueError("Schema columns must be JSON objects")
        name = column.get("name", "")
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name) or name in names:
            raise ValueError("Schema column names must be unique identifiers")
        if column.get("type") not in ("string", "integer", "decimal", "boolean"):
            raise ValueError("Unsupported schema column type")
        if column.get("role") not in ("input", "expected"):
            raise ValueError("Each column needs input or expected role")
        if not isinstance(column.get("nullable", False), bool):
            raise ValueError("nullable must be a boolean")
        tokens = column.get("null_tokens", [])
        if not isinstance(tokens, list) or not all(isinstance(token, str) for token in tokens):
            raise ValueError("null_tokens must be a list of strings")
        normalization = column.get("normalization")
        if normalization is not None:
            if (column["type"] != "string" or column["role"] != "expected" or not isinstance(normalization, dict)
                    or normalization.get("kind") != "java_type"
                    or not isinstance(normalization.get("aliases"), dict)):
                raise ValueError("Java type normalization requires a string column and explicit aliases")
            for alias, qualified in normalization["aliases"].items():
                if (not isinstance(alias, str) or not isinstance(qualified, str)
                        or not re.fullmatch(r"(?:[A-Za-z_$][\w$]*\.)+[A-Za-z_$][\w$]*", qualified)
                        or alias not in (qualified, qualified.rsplit(".", 1)[-1])):
                    raise ValueError("Only a simple Java name may alias its explicit fully qualified type")
        names.append(name)
    if {c["role"] for c in columns} != {"input", "expected"}:
        raise ValueError("Schema must contain both input and expected columns")
    if header is not None and names != header:
        raise ValueError("Model schema changed the supplied header")
    return columns


def header(path):
    return next(csv.reader(io.StringIO(path.read_text(encoding="utf-8-sig"))), [])


def canonical(value, column, normalize=True):
    if column.get("nullable") and value in column.get("null_tokens", []):
        return None
    kind = column["type"]
    try:
        if kind == "integer":
            if not re.fullmatch(r"[+-]?\d+", value):
                raise ValueError("Invalid integer")
            return str(int(value))
        if kind == "decimal":
            number = Decimal(value)
            if not number.is_finite():
                raise ValueError("Non-finite decimal")
            return format(number.normalize(), "f")
        if kind == "boolean":
            if value.lower() not in ("true", "false"):
                raise ValueError("Boolean must be true or false")
            return value.lower()
        if normalize and column.get("normalization"):
            return column["normalization"]["aliases"].get(value, value)
        return value
    except (InvalidOperation, ValueError):
        raise ValueError(f"Invalid {kind} value in column {column['name']}") from None


def read(path, schema, normalize=True):
    columns = validate_schema(schema)
    reader = csv.DictReader(io.StringIO(path.read_text(encoding="utf-8-sig")))
    if reader.fieldnames != [column["name"] for column in columns]:
        raise ValueError("CSV header differs from generated schema")
    inputs = [c["name"] for c in columns if c["role"] == "input"]
    expected = [c["name"] for c in columns if c["role"] == "expected"]
    result = {}
    for row in reader:
        if None in row or any(value is None for value in row.values()):
            raise ValueError("Malformed CSV row")
        parsed = {c["name"]: canonical(row[c["name"]], c, normalize) for c in columns}
        key = tuple(parsed[name] for name in inputs)
        if key in result:
            raise ValueError("Duplicate input combination in CSV")
        result[key] = {name: parsed[name] for name in expected}
    if not result:
        raise ValueError("CSV must contain cases; a header-only template is not evidence")
    return result


def check_frozen(directory, target=None):
    receipt = json.loads((directory / "receipt.json").read_text())
    if digest(directory / "cases.csv") != receipt["sha256"]:
        raise ValueError("Frozen human CSV changed")
    if target and receipt.get("target_class") not in (None, target):
        raise ValueError("Human CSV receipt belongs to another class")
    return receipt


def compare(human, ai, schema):
    left, right = read(human, schema), read(ai, schema)
    original_left, original_right = read(human, schema, False), read(ai, schema, False)
    inputs = [c["name"] for c in schema["columns"] if c["role"] == "input"]
    shared = left.keys() & right.keys()
    encode = lambda key: dict(zip(inputs, key))
    ordered = lambda keys: sorted(keys, key=repr)
    return {"human_sha256": digest(human), "ai_sha256": digest(ai),
            "human_cases": len(left), "ai_cases": len(right), "matching_inputs": len(shared),
            "matching_outcomes": sum(left[key] == right[key] for key in shared),
            "disagreements": [{"input": encode(key), "human": left[key], "ai": right[key]}
                              for key in ordered(shared) if left[key] != right[key]],
            "missing_from_ai": [encode(key) for key in ordered(left.keys() - right.keys())],
            "extra_in_ai": [encode(key) for key in ordered(right.keys() - left.keys())],
            "normalization_rules": {c["name"]: c["normalization"] for c in schema["columns"] if c.get("normalization")},
            "representation_differences": [
                {"input": encode(key), "human": original_left[key], "ai": original_right[key], "normalized": left[key]}
                for key in ordered(shared) if left[key] == right[key] and original_left[key] != original_right[key]],
            "limitation": "Input agreement is not model accuracy; inspect requirements, assertions and execution."}


def raw_metrics(directory, fqcn):
    totals = {key: 0 for key in ("tests", "failures", "errors", "skipped")}
    for path in (directory / "surefire-reports").glob("TEST-*.xml"):
        suite = ET.parse(path).getroot()
        for key in totals:
            totals[key] += int(suite.get(key, "0"))
    coverage = {}
    xml = directory / "site/jacoco/jacoco.xml"
    if xml.exists():
        node = ET.parse(xml).getroot().find(f".//class[@name='{fqcn.replace('.', '/')}']")
        if node is not None:
            coverage = {item.get("type"): {"covered": int(item.get("covered")),
                        "missed": int(item.get("missed"))} for item in node.findall("counter")}
    return totals, coverage


def reconcile(directory, fqcn, human, ai, schema, comparison, harness):
    """Re-read CSV/XML instead of trusting summaries; mismatches make the stage fail."""
    checks, rows = [], {}
    recomputed = compare(human, ai, schema)
    checks.append({"check": "CSV comparison matches raw datasets", "passed": recomputed == comparison})
    for name, csv_path in (("human", human), ("ai", ai)):
        run = json.loads((directory / name / "run.json").read_text())
        totals, coverage = raw_metrics(directory / name, fqcn)
        checks.extend([
            {"check": name + " target matches selected class", "passed": run.get("target_class") == fqcn},
            {"check": name + " JUnit totals match summary", "passed": all(run.get(k) == v for k, v in totals.items())},
            {"check": name + " test count matches CSV rows", "passed": totals["tests"] == len(read(csv_path, schema))},
            {"check": name + " JaCoCo counters match summary", "passed": run.get("target_coverage", {}) == coverage},
            {"check": name + " CSV hash matches executed input", "passed": run.get("csv_sha256") == digest(csv_path)},
            {"check": name + " identical harness executed", "passed": run.get("test_sha256", {}).get(harness.name) == digest(harness)},
        ])
        rows[name] = {**totals, "coverage": coverage, "execution_passed": run.get("passed", False)}
    return {"target_class": fqcn, "checks": checks, "consistent": all(c["passed"] for c in checks),
            "executions": rows, "comparison": recomputed}


def report(result):
    def coverage(row, metric):
        counter = row["coverage"].get(metric)
        if not counter or counter["covered"] + counter["missed"] == 0:
            return "N/A"
        total = counter["covered"] + counter["missed"]
        return f"{counter['covered']}/{total} ({100 * counter['covered'] / total:.1f}%)"
    human, ai = result["executions"]["human"], result["executions"]["ai"]
    comparison = result["comparison"]
    lines = ["# AI-4 — Đối chiếu dữ liệu và báo cáo thực thi", "", f"Class: `{result['target_class']}`", "",
             "| Chỉ số | Người viết | AI |", "|---|---:|---:|"]
    for label, key in (("Số dòng CSV", None), ("Tests", "tests"), ("Failures", "failures"),
                       ("Errors", "errors"), ("Skipped", "skipped")):
        lines.append(f"| {label} | {human[key] if key else comparison['human_cases']} | {ai[key] if key else comparison['ai_cases']} |")
    for metric in ("LINE", "BRANCH"):
        lines.append(f"| {metric} | {coverage(human, metric)} | {coverage(ai, metric)} |")
    lines += ["", f"Input chung: {comparison['matching_inputs']}; expected khớp: {comparison['matching_outcomes']}; "
              f"mâu thuẫn: {len(comparison['disagreements'])}.", "",
              f"Khác cách biểu diễn nhưng cùng expected sau chuẩn hóa: {len(comparison.get('representation_differences', []))}.", "",
              f"Chỉ có ở người viết: {len(comparison['missing_from_ai'])}; chỉ có ở AI: {len(comparison['extra_in_ai'])}.", "",
              f"Lượt Java: người viết={'PASS' if human.get('execution_passed') else 'FAIL'}; "
              f"AI={'PASS' if ai.get('execution_passed') else 'FAIL'}.", "",
              f"Đối chiếu CSV/Surefire/JaCoCo/hash: {'PASS' if result['consistent'] else 'FAIL'}.", ""]
    lines += [f"- {'PASS' if c['passed'] else 'FAIL'}: {c['check']}" for c in result["checks"]]
    if comparison.get("normalization_rules"):
        lines += ["", "Quy tắc chuẩn hóa được khai báo rõ trong schema/normalization_rules; "
                  "chỉ ánh xạ tên Java ngắn sang đúng class đầy đủ, không bỏ package một cách tổng quát."]
    lines += ["", "Nguồn chi tiết: `comparison.json`, `reconciliation.json`, `human/`, `ai/`.", "",
              "Độc lập của dữ liệu người dựa trên khai báo. Schema/harness do AI hỗ trợ và cần người review.",
              "Khớp input không phải accuracy; coverage cao/test xanh không chứng minh đặc tả hoặc assertion đúng.", ""]
    return "\n".join(lines)
