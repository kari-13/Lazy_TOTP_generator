import pytest
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "lazytotp"))

import oath as oath_module


@pytest.fixture
def oath():
    oath_module.load()
    return oath_module


@pytest.fixture
def rfc_key():
    return b"12345678901234567890"


@pytest.fixture
def rfc_key_sha256():
    return b"12345678901234567890123456789012"


@pytest.fixture
def rfc_key_sha512():
    return b"1234567890123456789012345678901234567890123456789012345678901234"
