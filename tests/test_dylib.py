from ctypes import *
from pathlib import Path
import pytest

current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent

lib = CDLL(parent_dir / "liboath.dylib")

lib.oath_init.restype = c_int
lib.oath_totp_generate.argtypes = [
    c_char_p,
    c_size_t,
    c_longlong,
    c_uint,
    c_longlong,
    c_uint,
    c_char_p,
]
lib.oath_totp_generate.restype = c_int

lib.oath_done.restype = c_int


@pytest.fixture(scope="module", autouse=True)
def oath_library():
    # Initialize liboath before the tests
    result = lib.oath_init()
    assert result == 0, f"oath_init() failed with {result}"

    yield

    # Clean up after all tests in this module
    lib.oath_done()


def test_totp_rfc6238():
    secret = b"12345678901234567890"

    tests = [
        (59, 8, "94287082"),
        (1111111109, 8, "07081804"),
        (1111111111, 8, "14050471"),
        (1234567890, 8, "89005924"),
        (2000000000, 8, "69279037"),
        (20000000000, 8, "65353130"),
    ]

    for timestamp, digits, expected in tests:
        otp = create_string_buffer(digits + 1)

        ret = lib.oath_totp_generate(
            secret,
            len(secret),
            timestamp,
            30,
            0,
            digits,
            otp,
        )

        assert ret == 0, f"liboath returned {ret}"
        assert otp.value.decode() == expected, (
            f"Timestamp {timestamp}: "
            f"expected {expected}, got {otp.value.decode()}"
        )

def test_totp_six_digits():
    secret = b"12345678901234567890"

    otp = create_string_buffer(7)

    ret = lib.oath_totp_generate(
        secret,
        len(secret),
        59,
        30,
        0,
        6,
        otp,
    )

    assert ret == 0
    assert otp.value.decode() == "287082"
