import os
import base64
import secrets
from argon2 import low_level
from cryptography.fernet import Fernet
import keyring


class Crypto:
    """
    A class for encrypting and decrypting data using Argon2id and Fernet.

    Provides methods to derive a key, encrypt a secret, and decrypt an encrypted value.
    It also handles retrieving or creating a salt from the operating system's keyring.
    """
    def __init__(self, password: str, secret: str):
        """
        Initializes a Crypto object with a password and a secret.

        Args:
            password (str): The password to use for key derivation.
            secret (str): The secret value to be encrypted.
        """
        self.password = password
        self.secret = secret
        self.key = None
        self.salt = None

    def derive_key(self, salt: bytes | None = None) -> bytes:
        """
        Derives a Fernet-compatible key from the password using Argon2id.

        Args:
            salt (bytes | None, optional): The salt to use. If None, a new salt is generated. Defaults to None.

        Returns:
            bytes: The derived Fernet key in base64 encoded format.
        """

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
        """
        Encrypts the secret value using Fernet with the derived key.

        Returns:
            bytes: The encrypted secret value.
        """
        if self.key is None:
            raise ValueError("Key has not been derived.")

        cipher = Fernet(self.key)
        return cipher.encrypt(self.secret.encode("utf-8"))

    def decrypt(self, encrypted_thing: bytes) -> str:
        """
        Decrypts the encrypted secret value using Fernet with the derived key.

        Args:
            encrypted_thing (bytes): The encrypted secret value to decrypt.

        Returns:
            str: The decrypted secret value.
        """
        if self.key is None:
            raise ValueError("Key has not been derived.")

        cipher = Fernet(self.key)
        return cipher.decrypt(encrypted_thing).decode("utf-8")

    def create_get_salt(user: str = "user"):
        """
        Retrieves or creates a salt from the OS's keyring (e.g., macOS Keychain, Windows Credential Manager, GNOME Keyring, KWallet) for 'lazy_totp'.  If the salt doesn't exist, it generates a new one and stores it in the keyring under the key 'lazy_totp' with the user specified as the username.
        """

        check = keyring.get_password("lazy_totp", user)
        if check is None:
            salt = secrets.token_bytes(16)
            keyring.set_password(
                "lazy_totp", "user", base64.urlsafe_b64encode(salt).decode("utf-8")
            )
            return salt
        if check is not None:
            return check
