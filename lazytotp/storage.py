from pathlib import Path
import tempfile
import json
class Storage:
    def __init__(self,**kwargs) -> None:
        self.data = kwargs
        self.path = Path("vault.json")
    def write(self):
        with open('Vault.json','w') as v :
            json.dump(self.kwargs,v)
    def add(self):
        with ooo
