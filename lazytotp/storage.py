
from pathlib import Path
import json
import time
import tempfile
import os


class Storage:
    def __init__(self, path: str | Path = "vault.json", **kwargs) -> None:
        self.path = Path(path)
        self.data: dict = {}

        # Ensure the parent directory exists
        self.path.parent.mkdir(parents=True, exist_ok=True)

        # Load existing vault
        if self.path.exists():
            try:
                with self.path.open("r", encoding="utf-8") as f:
                    loaded_data = json.load(f)

                if not isinstance(loaded_data, dict):
                    raise ValueError("Vault must contain a JSON object.")

                self.data = loaded_data

            except json.JSONDecodeError as e:
                raise ValueError(
                    f"Vault contains invalid JSON: {self.path}"
                ) from e

        # Overlay parameters on loaded data
        self.data.update(kwargs)

    def write(self) -> None:
        """Atomically saves the current data state to disk."""

        self.data["timestamp"] = int(time.time())

        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                dir=self.path.parent,
                prefix=f".{self.path.name}.",
                suffix=".tmp",
                delete=False,
                encoding="utf-8"
            ) as tmp:

                temp_path = Path(tmp.name)

                # Restrict access to the temporary file
                os.chmod(temp_path, 0o600)

                json.dump(self.data, tmp, indent=4)

                tmp.flush()
                os.fsync(tmp.fileno())

            # Atomic replacement
            os.replace(temp_path, self.path)
            temp_path = None

            # Ensure final file permissions
            os.chmod(self.path, 0o600)

            # Sync directory metadata where supported
            if hasattr(os, "O_DIRECTORY"):
                dir_fd = os.open(self.path.parent, os.O_RDONLY | os.O_DIRECTORY)
                try:
                    os.fsync(dir_fd)
                finally:
                    os.close(dir_fd)

        finally:
            # Remove leftover temporary files
            if temp_path is not None and temp_path.exists():
                temp_path.unlink()

    def add(self, **kwargs) -> None:
        """Merges new key-value pairs and writes to disk."""

        self.data.update(kwargs)
        self.write()

    def does_vault_exists(self) -> bool:
        """Returns True if the vault file exists on disk."""

        return self.path.is_file()

    def remove(self, key: str) -> bool:
        """Removes a key and saves changes. Returns False if missing."""

        if key not in self.data:
            return False

        del self.data[key]
        self.write()
        return True
