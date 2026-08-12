from ctypes import *
import base64
import time

lib = CDLL('liboath.dylib')
assert lib.oath_init() == 0
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
secret = base64.b32decode("JBSWY3DPEHPK3PXP")
otp = create_string_buffer(7)
ret = lib.oath_totp_generate(secret,
    len(secret),
    int(time.time()),
    30,
    0,
    6,
    otp
)

print("Return:", ret)
print("OTP:", otp.value.decode())


def test_totp():
    secret = b"12345678901234567890"

    otp = create_string_buffer(9)

    ret = lib.oath_totp_generate(
        secret,
        len(secret),
        59,
        30,
        0,
        8,
        otp
    )

    assert ret == 0
    assert otp.value.decode() == "94287082"

    print("✅ Test passed")
test_totp()
lib.oath_done()
