import ctypes
import ctypes.util
import os
import time as _time
from ctypes import c_char_p, c_int, c_uint,c_size_t, c_long, create_string_buffer

__all__ = ["load", "OathError", "totp_generate", "DEFAULT_STEP", "DEFAULT_DIGITS"]

DEFAULT_STEP = 30
DEFAULT_DIGITS = 6

_lib = None


class OathError(Exception):
    def __init__(self, code):
        self.code = code
        super().__init__(f"liboath error code: {code}")


def load(path=None):
    """Load liboath dynamic library across macOS, Linux, or Windows."""
    global _lib
    if path is None:
        path = (os.environ.get("LIBOATH_PATH")
                or ctypes.util.find_library("oath")
                or next((p for p in ("liboath.dylib", "liboath.0.dylib", "liboath.so", "liboath.dll",
                                     "/opt/homebrew/lib/liboath.dylib",
                                     "/usr/local/lib/liboath.dylib") if os.path.exists(p)), None))
        if path is None:
            raise OSError("liboath dynamic library not found.")

    _lib = ctypes.CDLL(path)
    _declare()
    return _lib


def _declare():
    TT = c_long  # time_t
    # oath_totp_generate(secret, secret_len, now, time_step, start_offset, digits, output_otp)
    _lib.oath_totp_generate.argtypes = [c_char_p, c_size_t, TT, c_uint, TT, c_uint, c_char_p]
    _lib.oath_totp_generate.restype = c_int


def _need():
    if _lib is None:
        load()
    return _lib


def _sanitize_and_decode_base32(secret_str: str) -> bytes:
    """Sanitize input string and decode Base32 using Python's native module."""
    import base64
    # Clean up spaces, hyphens, and normalize casing
    cleaned = secret_str.replace(" ", "").replace("-", "").upper()
    # Add Base32 padding if missing
    missing_padding = len(cleaned) % 8
    if missing_padding:
        cleaned += "=" * (8 - missing_padding)
    return base64.b32decode(cleaned)


def totp_generate(secret, now=None, step=DEFAULT_STEP, start_offset=0, digits=DEFAULT_DIGITS) -> str:
    """
    Generate a TOTP token string.
    `secret` can be a raw bytes object or a Base32 string (e.g., "JBSW Y3DP EHPK 3PXP").
    """
    if isinstance(secret, str):
        secret_bytes = _sanitize_and_decode_base32(secret)
    else:
        secret_bytes = bytes(secret)

    now_ts = int(_time.time()) if now is None else int(now)
    out_buf = create_string_buffer(digits + 1)

    rc = _need().oath_totp_generate(
        secret_bytes,
        len(secret_bytes),
        now_ts,
        step,
        start_offset,
        digits,
        out_buf
    )

    if rc < 0:
        raise OathError(rc)

    return out_buf.value.decode("ascii")


if __name__ == "__main__":
    # Test vector run
    load()
    print("Generated TOTP:", totp_generate("JBSW Y3DP EHPK 3PXP"))
