from unittest.mock import MagicMock, patch
import os
from pathlib import Path
import pytest
import sys
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "lazytotp"))
import oath
from oath import (totp_generate,
    _sanitize_and_decode_base32,
    OathError,
    load,
    DEFAULT_STEP,
    DEFAULT_DIGITS,)


# =====================================================================
# Secret Sanitization & Base32 Decoding Tests
# =====================================================================

def test_clean_base32_string():
    secret = "JBSWY3DPEHPK3PXP"
    decoded = _sanitize_and_decode_base32(secret)
    assert isinstance(decoded, bytes)
    assert decoded == b"Hello!\xde\xad\xbe\xef"


@pytest.mark.parametrize("raw_input", [
    "jbsw y3dp ehpk 3pxp",
    "JBSW-Y3DP-EHPK-3PXP",
    "  jbswy3dpehpk3pxp  ",
    "jbsw-y3dp ehpk3pxp",
])
def test_sanitization_formatting_variations(raw_input):
    expected_bytes = _sanitize_and_decode_base32("JBSWY3DPEHPK3PXP")
    assert _sanitize_and_decode_base32(raw_input) == expected_bytes


def test_missing_padding_handling():
    # Unpadded base32 string ("JBSWY3DPEHPK3PX" missing '=')
    unpadded = "JBSWY3DPEHPK3PX"
    decoded = _sanitize_and_decode_base32(unpadded)
    assert isinstance(decoded, bytes)


def test_invalid_base32_character_raises():
    with pytest.raises(Exception):
        _sanitize_and_decode_base32("INVALID_BASE32_!!!")


# =====================================================================
# TOTP Generation Tests (Mocking C Library)
# =====================================================================

@pytest.fixture
def mock_c_lib():
    """Fixture that mocks the underlying C library loaded by _need()."""
    with patch("oath._need") as mock_need:
        mock_lib = MagicMock()
        mock_need.return_value = mock_lib
        yield mock_lib


def test_successful_generation_from_string(mock_c_lib):
    def fake_c_totp(secret, secret_len, now, step, start_offset, digits, out_buf):
        out_buf.value = b"123456"
        return 0  # Success code in liboath

    mock_c_lib.oath_totp_generate.side_effect = fake_c_totp

    result = totp_generate("JBSWY3DPEHPK3PXP", now=1700000000)
    assert result == "123456"

    # Verify parameters passed to the C library
    mock_c_lib.oath_totp_generate.assert_called_once()
    args = mock_c_lib.oath_totp_generate.call_args[0]
    assert args[2] == 1700000000  # timestamp
    assert args[3] == DEFAULT_STEP
    assert args[5] == DEFAULT_DIGITS


def test_successful_generation_from_bytes(mock_c_lib):
    def fake_c_totp(secret, secret_len, now, step, start_offset, digits, out_buf):
        out_buf.value = b"654321"
        return 0

    mock_c_lib.oath_totp_generate.side_effect = fake_c_totp

    raw_bytes = b"12345678901234567890"
    result = totp_generate(raw_bytes, now=1700000000)
    assert result == "654321"


def test_custom_parameters(mock_c_lib):
    def fake_c_totp(secret, secret_len, now, step, start_offset, digits, out_buf):
        out_buf.value = b"12345678"
        return 0

    mock_c_lib.oath_totp_generate.side_effect = fake_c_totp

    result = totp_generate("JBSWY3DPEHPK3PXP", now=1000, step=60, start_offset=10, digits=8)
    assert result == "12345678"

    args = mock_c_lib.oath_totp_generate.call_args[0]
    assert args[2] == 1000  # now
    assert args[3] == 60    # step
    assert args[4] == 10    # start_offset
    assert args[5] == 8     # digits


def test_library_error_raises_oath_error(mock_c_lib):
    # Simulate a liboath error code return
    mock_c_lib.oath_totp_generate.return_value = -1

    with pytest.raises(OathError) as exc_info:
        totp_generate("JBSWY3DPEHPK3PXP")

    assert exc_info.value.code == -1


# =====================================================================
# Library Loader Tests
# =====================================================================

def test_missing_library_raises_os_error():
    with patch("os.path.exists", return_value=False), \
         patch("ctypes.util.find_library", return_value=None), \
         patch.dict(os.environ, {}, clear=True):

        oath._lib = None
        with pytest.raises(OSError, match="liboath dynamic library not found."):
            load()


@patch("ctypes.CDLL")
def test_successful_load_custom_path(mock_cdll):
    oath._lib = None
    mock_instance = MagicMock()
    mock_cdll.return_value = mock_instance

    lib = load("/custom/path/liboath.dylib")
    assert lib == mock_instance
    mock_cdll.assert_called_once_with("/custom/path/liboath.dylib")
