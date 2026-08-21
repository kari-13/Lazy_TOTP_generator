from pathlib import Path
import tempfile
import json
class Storage:
    def __init__(self,**kwargs) -> None:
        self.kwargs = kwargs
    def write(self):
        with open('Vault.json','w') as v :
            json.dump(self.kwargs,v)
