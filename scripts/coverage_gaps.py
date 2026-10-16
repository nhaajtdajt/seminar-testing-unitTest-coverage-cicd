#!/usr/bin/env python3
"""Extract missed source lines/branches from JaCoCo XML, without guessing branch predicates."""
import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET

def extract(path, source_root=None):
    result = []
    for package in ET.parse(path).getroot().findall("package"):
        for source in package.findall("sourcefile"):
            relative = Path(package.attrib["name"]) / source.attrib["name"]
            text = []
            if source_root:
                root = Path(source_root).resolve()
                candidate = (root / relative).resolve()
                if candidate.is_relative_to(root) and candidate.is_file():
                    text = candidate.read_text().splitlines()
            for line in source.findall("line"):
                number = int(line.attrib["nr"])
                missed_branches = int(line.attrib["mb"])
                missed_instructions = int(line.attrib["mi"])
                if missed_branches or missed_instructions:
                    result.append({"file": relative.as_posix(), "line": number,
                        "missed_branches": missed_branches, "covered_branches": int(line.attrib["cb"]),
                        "missed_instructions": missed_instructions,
                        "source": text[number-1].strip() if 0 < number <= len(text) else None})
    return {"report": str(path), "note": "XML reports branch counts, not exact true/false predicates; inspect source to propose tests.", "gaps": result}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xml", type=Path)
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = json.dumps(extract(args.xml, args.source_root), ensure_ascii=False, indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(data)
    else:
        print(data, end="")

if __name__ == "__main__":
    main()
