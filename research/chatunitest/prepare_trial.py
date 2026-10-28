#!/usr/bin/env python3
"""Prepare a disposable copy for the author's current plugin; never edit the source project."""
import argparse
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("destination", type=Path)
args = parser.parse_args()
if args.destination.exists():
    parser.error("Choose a fresh destination")
shutil.copytree(ROOT/"case-study", args.destination, ignore=shutil.ignore_patterns("target", "__pycache__"))
# The main POM has an additional test-resource directory relative to the repo root.
# Copy AI data to the disposable project instead of referencing personal paths.
shutil.copytree(ROOT/"ai/data", args.destination/"src/test/resources", dirs_exist_ok=True)
tree = ET.parse(args.destination/"pom.xml")
plugin = ET.parse(Path(__file__).with_name("pom.fragment.xml")).getroot()
for element in plugin.iter():
    element.tag = "{"+NS+"}"+element.tag
tree.getroot().find(f"{{{NS}}}build/{{{NS}}}plugins").append(plugin)
tree.write(args.destination/"pom.xml", encoding="unicode", xml_declaration=True)
print(f"Prepared {args.destination}; original project was not modified.")
