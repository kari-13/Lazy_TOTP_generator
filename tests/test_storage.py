import json
import time
from pathlib import Path

import pytest

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "lazytotp"))

from storage import Storage


@pytest.fixture
def storage(tmp_path, monkeypatch):
    """
    Create a Storage instance whose vault.json lives
    inside pytest's temporary directory.
    """
    monkeypatch.chdir(tmp_path)
    return Storage(
        username="test_user",
        salt="test_salt",
        encrypted_secret="encrypted_data",
    )


def test_write_creates_file(storage):
    storage.write()

    path = Path("vault.json")

    assert path.exists()

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["username"] == "test_user"
    assert data["salt"] == "test_salt"
    assert data["encrypted_secret"] == "encrypted_data"
    assert "timestamp" in data


def test_add_new_value(storage):
    storage.write()
    storage.add(password="encrypted_password")

    with Path("vault.json").open("r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["password"] == "encrypted_password"


def test_add_preserves_existing_data(storage):
    storage.write()

    storage.add(password="encrypted_password")

    with Path("vault.json").open("r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["username"] == "test_user"
    assert data["salt"] == "test_salt"
    assert data["encrypted_secret"] == "encrypted_data"
    assert data["password"] == "encrypted_password"


def test_add_updates_existing_value(storage):
    storage.write()

    storage.add(username="new_user")

    with Path("vault.json").open("r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["username"] == "new_user"


def test_timestamp_updates(storage):
    storage.write()

    with Path("vault.json").open("r", encoding="utf-8") as f:
        first = json.load(f)

    time.sleep(1)

    storage.add(test_value="hello")

    with Path("vault.json").open("r", encoding="utf-8") as f:
        second = json.load(f)

    assert second["timestamp"] > first["timestamp"]


def test_atomic_write_leaves_no_temp_file(storage):
    storage.write()

    path = Path("vault.json")

    temp_files = list(
        path.parent.glob(f".{path.name}.*.tmp")
    )

    assert temp_files == []


def test_multiple_values_can_be_added(storage):
    storage.write()

    storage.add(
        password="password123",
        website="github.com",
        notes="test account",
    )

    with Path("vault.json").open("r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["password"] == "password123"
    assert data["website"] == "github.com"
    assert data["notes"] == "test account"
