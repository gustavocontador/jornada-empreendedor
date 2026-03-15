"""
Minimal test to validate pytest execution in CI.

This test doesn't import anything from app to avoid dependency issues.
"""


def test_pytest_works():
    """Simplest possible test - just verify pytest runs."""
    assert True


def test_basic_math():
    """Basic arithmetic to ensure Python works."""
    assert 1 + 1 == 2
    assert 10 * 5 == 50
