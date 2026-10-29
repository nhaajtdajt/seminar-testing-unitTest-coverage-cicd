#!/usr/bin/env python3
"""Clean generated Java/source copies/debug payloads from local AI output, never real src or CSV."""
import argparse
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
PAYLOADS = {"request.json", "response.json", "parsed-response.json", "prompt.md"}


def allowed_roots():
    return [ROOT / ".ai-work", ROOT / "evidence/tuan-06/gemini-live"]


def plan(roots):
    projects, files = [], []
    originals = allowed_roots()
    if any(base.is_symlink() or not base.resolve().is_relative_to(ROOT.resolve()) for base in originals):
        raise ValueError("Allowed AI workspaces must stay inside the repository without symlinks")
    bases = [base.resolve() for base in originals]
    for raw in roots:
        if raw.is_symlink():
            raise ValueError("Refusing a symlink workspace")
        root = raw.resolve()
        if not any(root.is_relative_to(base) for base in bases):
            raise ValueError("Cleanup is restricted to .ai-work and legacy gemini-live output")
        if not root.exists():
            continue
        entries = list(root.rglob("*"))
        if any(path.is_symlink() for path in entries):
            raise ValueError("Refusing cleanup through symlinks; inspect that workspace manually")
        candidates = sorted([p for p in entries if p.is_dir() and p.name == "project" and p.parent.name == "inputs"
                             and (p / "pom.xml").is_file() and (p / "mvnw").is_file()], key=lambda p: len(p.parts))
        copies = []
        for path in candidates:
            if not any(path.is_relative_to(parent) for parent in copies):
                copies.append(path)
        projects.extend(copies)
        for path in entries:
            if not path.is_file() or any(path.is_relative_to(copy) for copy in copies):
                continue
            relative = path.relative_to(root)
            if (path.suffix == ".java" and "generated" in relative.parts) or path.name in PAYLOADS:
                files.append(path)
    projects = sorted(set(projects))
    files = sorted(set(files))
    return projects, files


def clean(roots, apply=False):
    projects, files = plan(roots)
    count = len(files) + sum(sum(p.is_file() for p in project.rglob("*")) for project in projects)
    size = sum(p.stat().st_size for p in files)
    size += sum(p.stat().st_size for project in projects for p in project.rglob("*") if p.is_file())
    print(f"{'CLEAN' if apply else 'PREVIEW'}: {len(projects)} copied projects, {len(files)} generated/payload files; "
          f"{count} files total, {size} bytes")
    for path in (projects + files)[:12]:
        print(path.relative_to(ROOT.resolve()))
    if apply:
        for path in files:
            path.unlink()
        for project in projects:
            shutil.rmtree(project)
        print("Cleaned local source/payloads. CSV, receipt, reports, real src and key config preserved.")
    else:
        print("Nothing deleted. Add --apply after finishing AI-1/AI-2/AI-4.")
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, help="Optional output subdirectory within an allowed workspace")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        clean([args.root] if args.root else allowed_roots(), args.apply)
        return 0
    except (ValueError, OSError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    sys.exit(main())
