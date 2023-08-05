import pytest
import sequtil


def test_project_defines_author_and_version():
    assert hasattr(sequtil, '__author__')
    assert hasattr(sequtil, '__version__')
