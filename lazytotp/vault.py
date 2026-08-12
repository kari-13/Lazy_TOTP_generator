class Vault:
    def __init__(self,account,secret,salt):
        self.account = account
        self.secret = secret
        self.salt = salt
