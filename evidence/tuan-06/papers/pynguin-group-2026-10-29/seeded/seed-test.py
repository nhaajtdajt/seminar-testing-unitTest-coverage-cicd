import pathlib
import scripts.coverage_gaps as module_0

def test_empty_report():
    path = pathlib.Path('/tmp/ga-paper-pynguin-group-seeded/empty.xml')
    result = module_0.extract(path)
    assert result["gaps"] == []
