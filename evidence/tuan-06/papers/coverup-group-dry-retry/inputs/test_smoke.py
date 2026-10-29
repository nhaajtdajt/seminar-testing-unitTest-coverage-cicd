from pathlib import Path
from scripts.coverage_gaps import extract
def test_empty_report(tmp_path):
    xml = tmp_path/'jacoco.xml'
    xml.write_text('<report/>')
    assert extract(xml)['gaps'] == []
