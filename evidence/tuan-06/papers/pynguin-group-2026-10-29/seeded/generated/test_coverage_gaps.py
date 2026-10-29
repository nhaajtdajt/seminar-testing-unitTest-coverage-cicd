#  This file was automatically generated using Pynguin.

import sys
import scripts.coverage_gaps

coverage_gaps_ = sys.modules["scripts.coverage_gaps"]
import pathlib


def test_0():
    import pathlib

    var_0 = pathlib.Path("/tmp/ga-paper-pynguin-group-seeded/empty.xml")
    coverage_gaps_.extract(var_0)


def test_1():
    import pathlib

    var_22 = pathlib.Path("/tmp/ga-paper-pynguin-group-seeded/empty.xml")
    coverage_gaps_.extract(path=var_22)
