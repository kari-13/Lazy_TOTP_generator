import os
import base64

from argon2 import low_level
from cryptography.fernet import Fernet


class Crypto:
    def __init__(self, password: str, secret: str):
        self.password = password
        self.secret = secret
        self.key = None
        self.salt = None

    def derive_key(self, salt: bytes | None = None) -> bytes:
        """Derive a Fernet-compatible key from the password."""

        if salt is None:
            salt = os.urandom(16)

        self.salt = salt

        raw_key = low_level.hash_secret_raw(
            secret=self.password.encode("utf-8"),
            salt=salt,
            time_cost=3,
            memory_cost=65536,
            parallelism=4,
            hash_len=32,
            type=low_level.Type.ID,
        )

        self.key = base64.urlsafe_b64encode(raw_key)
        return self.key

    def encrypt(self) -> bytes:
        if self.key is None:
            raise ValueError("Key has not been derived.")

        cipher = Fernet(self.key)
        return cipher.encrypt(self.secret.encode("utf-8"))

    def decrypt(self, encrypted_thing: bytes) -> str:
        if self.key is None:
            raise ValueError("Key has not been derived.")

        cipher = Fernet(self.key)
        return cipher.decrypt(encrypted_thing).decode("utf-8")
