import pytest

from lazytotp.oath import OathConverter, OathError


LIB_PATH = "liboath.dylib"


@pytest.fixture
def oath():
    return OathConverter(LIB_PATH)


def test_encode_hello(oath):
    assert oath.bytes_to_base32(b"hello") == "NBSWY3DP"


def test_encode_foo(oath):
    assert oath.bytes_to_base32(b"foo") == "MZXW6==="


def test_empty_bytes(oath):
    assert oath.bytes_to_base32(b"") == ""


def test_binary_data(oath):
    result = oath.bytes_to_base32(b"\x00\x01\x02\xff")

    assert isinstance(result, str)
    assert all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567=" for c in result)


@pytest.mark.parametrize(
    "value",
    [
        "hello",
        bytearray(b"hello"),
        memoryview(b"hello"),
        123,
        None,
    ],
)
def test_rejects_non_bytes(oath, value):
    with pytest.raises(TypeError):
        oath.bytes_to_base32(value)


def test_invalid_library():
    with pytest.raises(OSError):
        OathConverter("does-not-exist.dylib")


def test_oath_error():
    error = OathError(42)

    assert error.return_code == 42
    assert str(error) == "liboath failed with error code: 42"
