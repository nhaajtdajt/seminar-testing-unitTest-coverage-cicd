# file: scripts/coverage_gaps.py:30-41
# asked: {"lines": [31, 32, 33, 34, 35, 36, 37, 38, 39, 41], "branches": [[37, 38], [37, 41]]}
# gained: {"lines": [31, 32, 33, 34, 35, 36, 37, 38, 39, 41], "branches": [[37, 38], [37, 41]]}

import json
import sys
from pathlib import Path
from scripts.coverage_gaps import main


def test_main_stdout(monkeypatch, capsys):
    fake_data = {"report": "test.xml", "gaps": []}

    def mock_extract(xml, source_root):
        assert xml == Path("test.xml")
        assert source_root is None
        return fake_data

    monkeypatch.setattr("scripts.coverage_gaps.extract", mock_extract)
    monkeypatch.setattr(sys, "argv", ["coverage_gaps", "test.xml"])

    main()

    captured = capsys.readouterr()
    expected = json.dumps(fake_data, ensure_ascii=False, indent=2) + "\n"
    assert captured.out == expected


def test_main_output_file(monkeypatch, tmp_path):
    fake_data = {"report": "test.xml", "gaps": [{"file": "a.py"}]}
    out_file = tmp_path / "nested" / "out.json"

    def mock_extract(xml, source_root):
        assert xml == Path("test.xml")
        assert source_root == Path("src")
        return fake_data

    monkeypatch.setattr("scripts.coverage_gaps.extract", mock_extract)
    monkeypatch.setattr(
        sys,
        "argv",
        ["coverage_gaps", "test.xml", "--source-root", "src", "--output", str(out_file)],
    )

    main()

    expected = json.dumps(fake_data, ensure_ascii=False, indent=2) + "\n"
    assert out_file.exists()
    assert out_file.read_text() == expected
