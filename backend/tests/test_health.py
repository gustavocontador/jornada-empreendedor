"""
Basic health check tests for backend.

This module contains minimal tests to validate CI/CD pipeline setup.
Comprehensive tests will be added in future stories.
"""
import pytest


def test_import_app():
    """Test that main app module can be imported."""
    from app import main

    assert main is not None


def test_basic_arithmetic():
    """Basic test to ensure pytest is working correctly."""
    assert 1 + 1 == 2
    assert 2 * 3 == 6


@pytest.mark.asyncio
async def test_async_functionality():
    """Basic async test to ensure pytest-asyncio is working."""
    async def async_add(a: int, b: int) -> int:
        return a + b

    result = await async_add(2, 3)
    assert result == 5
