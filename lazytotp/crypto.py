import os
from argon2 import low_level
import cryptography.Fernet
class Crypto:
    def __init__(self,password,secret):
        self.password = password
        self.secret = secret
    def Kdf(self):
        Fernet.
