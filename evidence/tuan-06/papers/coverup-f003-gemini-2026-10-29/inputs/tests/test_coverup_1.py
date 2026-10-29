# file: f003/__init__.py:4-13
# asked: {"lines": [9, 10, 11], "branches": [[8, 9], [10, 8], [10, 11]]}
# gained: {"lines": [9, 10, 11], "branches": [[8, 9], [10, 8], [10, 11]]}

from f003 import below_zero


def test_below_zero_returns_true_when_balance_drops_below_zero():
    assert below_zero([1, 2, -4, 5]) is True
    assert below_zero([-1]) is True
    assert below_zero([1, -1, 2, -3]) is True


def test_below_zero_returns_false_when_balance_remains_non_negative():
    assert below_zero([1, 2, 3]) is False
    assert below_zero([1, 2, -2, 1]) is False
    assert below_zero([]) is False
