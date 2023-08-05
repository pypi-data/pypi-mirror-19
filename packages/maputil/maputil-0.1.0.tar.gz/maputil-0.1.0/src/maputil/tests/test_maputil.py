import pytest
import maputil


def test_project_defines_author_and_version():
    assert hasattr(maputil, '__author__')
    assert hasattr(maputil, '__version__')
