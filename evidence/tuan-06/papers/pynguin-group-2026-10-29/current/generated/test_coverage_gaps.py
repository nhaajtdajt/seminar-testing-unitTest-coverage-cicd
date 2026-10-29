#  This file was automatically generated using Pynguin.

import pytest
import sys
import scripts.coverage_gaps

coverage_gaps_ = sys.modules["scripts.coverage_gaps"]


@pytest.mark.xfail(strict=True)
def test_0():
    coverage_gaps_.extract(path=bool)
