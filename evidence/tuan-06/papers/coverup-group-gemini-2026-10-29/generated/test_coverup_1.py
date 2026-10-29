# file: scripts/coverage_gaps.py:8-28
# asked: {"lines": [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], "branches": [[10, 11], [11, 10], [11, 12], [14, 15], [14, 19], [17, 18], [17, 19], [19, 11], [19, 20], [23, 19], [23, 24]]}
# gained: {"lines": [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], "branches": [[10, 11], [11, 10], [11, 12], [14, 15], [14, 19], [17, 18], [17, 19], [19, 11], [19, 20], [23, 19], [23, 24]]}

from pathlib import Path
import pytest
from scripts.coverage_gaps import extract


def test_extract_with_source_and_gaps(tmp_path):
    pkg_dir = tmp_path / "pkg"
    pkg_dir.mkdir()
    source_file = pkg_dir / "file.py"
    source_file.write_text("line 1\nline 2\nline 3\n")

    xml_content = """<?xml version="1.0"?>
<report>
    <package name="pkg">
        <sourcefile name="file.py">
            <line nr="1" mi="0" mb="0" cb="1"/>
            <line nr="2" mi="1" mb="0" cb="0"/>
            <line nr="5" mi="0" mb="1" cb="1"/>
        </sourcefile>
    </package>
</report>
"""
    xml_path = tmp_path / "report.xml"
    xml_path.write_text(xml_content)

    res = extract(xml_path, source_root=tmp_path)

    assert res["report"] == str(xml_path)
    assert "XML reports branch counts" in res["note"]
    assert len(res["gaps"]) == 2

    assert res["gaps"][0] == {
        "file": "pkg/file.py",
        "line": 2,
        "missed_branches": 0,
        "covered_branches": 0,
        "missed_instructions": 1,
        "source": "line 2",
    }
    assert res["gaps"][1] == {
        "file": "pkg/file.py",
        "line": 5,
        "missed_branches": 1,
        "covered_branches": 1,
        "missed_instructions": 0,
        "source": None,
    }


def test_extract_without_source_root(tmp_path):
    xml_content = """<?xml version="1.0"?>
<report>
    <package name="pkg">
        <sourcefile name="file.py">
            <line nr="1" mi="1" mb="0" cb="0"/>
        </sourcefile>
    </package>
</report>
"""
    xml_path = tmp_path / "report.xml"
    xml_path.write_text(xml_content)

    res = extract(xml_path, source_root=None)

    assert len(res["gaps"]) == 1
    assert res["gaps"][0]["source"] is None


def test_extract_missing_source_file(tmp_path):
    xml_content = """<?xml version="1.0"?>
<report>
    <package name="pkg">
        <sourcefile name="nonexistent.py">
            <line nr="1" mi="1" mb="0" cb="0"/>
        </sourcefile>
    </package>
</report>
"""
    xml_path = tmp_path / "report.xml"
    xml_path.write_text(xml_content)

    res = extract(xml_path, source_root=tmp_path)

    assert len(res["gaps"]) == 1
    assert res["gaps"][0]["source"] is None


def test_extract_no_gaps(tmp_path):
    xml_content = """<?xml version="1.0"?>
<report>
    <package name="pkg">
        <sourcefile name="file.py">
            <line nr="1" mi="0" mb="0" cb="1"/>
        </sourcefile>
    </package>
</report>
"""
    xml_path = tmp_path / "report.xml"
    xml_path.write_text(xml_content)

    res = extract(xml_path, source_root=tmp_path)

    assert res["gaps"] == []
