from pathlib import Path
import json
import time
import tempfile
import os


class Storage:
    def __init__(self, **kwargs) -> None:
        self.data = kwargs
        self.path = Path("vault.json")

    def write(self):
        # Always update timestamp before saving
        self.data["timestamp"] = int(time.time())

        # Create temporary file in the same directory
        with tempfile.NamedTemporaryFile(
            mode="w",
            dir=self.path.parent,
            prefix=f".{self.path.name}.",
            suffix=".tmp",
            delete=False,
            encoding="utf-8"
        ) as tmp:
            temp_path = Path(tmp.name)

            # Write JSON to temporary file
            json.dump(self.data, tmp, indent=4)

            # Make sure Python has pushed everything to the OS
            tmp.flush()
            os.fsync(tmp.fileno())

        # Atomically replace the old vault
        os.replace(temp_path, self.path)

    def add(self, **kwargs):
        # Load existing data if the vault exists
        if self.path.exists():
            with self.path.open("r", encoding="utf-8") as f:
                self.data = json.load(f)

        # Add/update values
        self.data.update(kwargs)

        # Atomically save everything
        self.write()
