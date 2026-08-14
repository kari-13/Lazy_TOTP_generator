import os

import pytest
from cryptography.fernet import InvalidToken

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "lazytotp"))

from crypto import Crypto


def test_encrypt_decrypt():
    crypto = Crypto("correct password", "hello world")
    crypto.derive_key()

    encrypted = crypto.encrypt()
    decrypted = crypto.decrypt(encrypted)

    assert decrypted == "hello world"


def test_same_password_same_salt():
    salt = os.urandom(16)

    a = Crypto("password", "secret")
    b = Crypto("password", "secret")

    a.derive_key(salt)
    b.derive_key(salt)

    assert a.key == b.key


def test_different_salt():
    a = Crypto("password", "secret")
    b = Crypto("password", "secret")

    a.derive_key(os.urandom(16))
    b.derive_key(os.urandom(16))

    assert a.key != b.key


def test_wrong_password():
    correct = Crypto("correct password", "secret")
    correct.derive_key()

    encrypted = correct.encrypt()

    wrong = Crypto("wrong password", "")
    wrong.derive_key(correct.salt)

    with pytest.raises(InvalidToken):
        wrong.decrypt(encrypted)


def test_tampering():
    crypto = Crypto("password", "secret")
    crypto.derive_key()

    encrypted = bytearray(crypto.encrypt())

    # Modify the ciphertext
    encrypted[-1] ^= 1

    with pytest.raises(InvalidToken):
        crypto.decrypt(bytes(encrypted))
