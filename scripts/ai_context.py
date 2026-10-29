"""Read Java context directly from src; persist fingerprints, never source trees."""
import hashlib
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
LITERALS = re.compile(r'"""[\s\S]*?"""|/\*[\s\S]*?\*/|//[^\n]*|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def discover(project=None):
    project = project or ROOT / "case-study"
    result = []
    for path in sorted((project / "src/main/java").rglob("*.java")):
        code = LITERALS.sub(" ", path.read_text())
        match = re.search(r"\bpackage\s+([\w.]+)\s*;", code)
        package = match.group(1) if match else ""
        for declaration in re.finditer(r"\b(class|record|enum|interface)\s+([\w$]+)", code):
            prefix = code[:declaration.start()]
            if prefix.count("{") != prefix.count("}"):
                continue  # Nested types are tested through their enclosing top-level class.
            kind, name = declaration.groups()
            result.append({"fqcn": f"{package}.{name}" if package else name,
                           "package": package, "name": name, "kind": kind,
                           "source": path.relative_to(project).as_posix()})
    return result


def select(name):
    matches = [item for item in discover() if name in (item["name"], item["fqcn"], item["source"])]
    if len(matches) != 1:
        raise ValueError("Class not found or ambiguous; use list-classes and pass its fully qualified name")
    return matches[0]


def related_sources(project, target):
    """Follow local type references/imports; no hand-maintained service registry."""
    types = discover(project)
    pending, seen = [target["source"]], set()
    while pending:
        relative = pending.pop()
        if relative in seen:
            continue
        seen.add(relative)
        code = LITERALS.sub(" ", (project / relative).read_text())
        package_match = re.search(r"\bpackage\s+([\w.]+)\s*;", code)
        package = package_match.group(1) if package_match else ""
        imports = re.findall(r"\bimport\s+(?:static\s+)?([\w.*$]+)\s*;", code)
        identifiers = set(re.findall(r"\b[\w$]+\b", code))
        for item in types:
            imported = any(value == item["fqcn"] or value.startswith(item["fqcn"] + ".")
                           or value == item["package"] + ".*" for value in imports)
            qualified = re.search(r"\b" + re.escape(item["fqcn"]) + r"\b", code)
            if item["name"] in identifiers and (item["package"] == package or imported or qualified):
                if item["source"] not in seen:
                    pending.append(item["source"])
    return [target["source"]] + sorted(seen - {target["source"]})


def manifest(project):
    files = [project / "pom.xml", project / "mvnw"]
    files += [p for p in (project / ".mvn").rglob("*") if p.is_file()]
    files += list((project / "src/main/java").rglob("*.java"))
    return {p.relative_to(project).as_posix(): sha(p) for p in files}


def check_project(project, expected):
    if manifest(project) != expected:
        raise ValueError("Production source/build inputs changed; generate a fresh baseline/schema")


def copy_project(source, destination, expected):
    """Only for the ephemeral Maven build; no standard tests, target or local config."""
    check_project(source, expected)
    destination.mkdir(parents=True)
    for name in ("pom.xml", "mvnw"):
        shutil.copy2(source / name, destination / name)
    shutil.copytree(source / ".mvn", destination / ".mvn")
    shutil.copytree(source / "src/main/java", destination / "src/main/java")
    check_project(destination, expected)


def snapshot(destination, target=None, previous=None, requirements=None, schema=None):
    """Compatibility name: save context/hash metadata, read the live project directly."""
    import gemini_client as client
    project = ROOT / "case-study"
    if previous:
        expected = json.loads((previous / "inputs/manifest.json").read_text())
        check_project(project, expected)
        context = json.loads((previous / "inputs/context.json").read_text())
        if target and target["fqcn"] != context["target"]["fqcn"]:
            raise ValueError("Target differs from baseline/schema source")
    else:
        expected = manifest(project)
        context = {"target": target, "requirements": requirements.read_text() if requirements else "",
                   "schema": schema.read_text() if schema else "", "schema_files": []}
        if not schema:
            for sql in sorted((project / "src/main/resources").rglob("*.sql")):
                ddl = [part.strip() for part in sql.read_text().split(";")
                       if re.search(r"\b(?:CREATE|ALTER)\s+TABLE\b", part, re.I)]
                if ddl:
                    context["schema_files"].append(sql.name)
                    context["schema"] += f"\nFile {sql.name}:\n" + ";\n".join(ddl)
        context["requirements_origin"] = "user_document" if requirements else "source_only; intent requires human review"
        context["context_source_files"] = related_sources(project, target)
    context["source_storage"] = "read directly from src; only build copies live in system temporary directory"
    client.save(destination / "inputs/manifest.json", expected)
    client.save(destination / "inputs/context.json", context)
    return project, context


def source_text(project, context):
    target = context["target"]
    paths = [project / relative for relative in context.get("context_source_files", related_sources(project, target))]
    text = "\n\n".join(f"File {p.relative_to(project)}:\n{p.read_text()}" for p in paths)
    if len(text.encode()) > 200_000:
        raise ValueError("Production source exceeds 200 KB; split the Maven module instead of silently truncating context")
    return text


def substitutions(project, context, class_name):
    target = context["target"]
    return {"TARGET_CLASS": target["fqcn"], "PACKAGE": target["package"], "CLASS_NAME": class_name,
            "SOURCE": source_text(project, context), "SCHEMA": context["schema"] or "Infer domain/DTO structure from source; no DDL supplied.",
            "REQUIREMENTS": context["requirements"] or
                "No independent requirements supplied. Infer observable behavior from source, distinguish assumptions, "
                "and do not claim the implementation proves the business requirements."}
