import subprocess
import sys

import pytest

import hermes as hr

RESOURCES = "hermes/connectors/lib/datasets/cpi.csv"


@pytest.fixture
def cli_storage(tmp_path):
    import hermes

    root = tmp_path / "store"
    hermes.configure(storage_root=str(root))
    ds = hermes.ingest(RESOURCES)
    hermes.save(ds, name="cli_proof", format="ipc")
    return str(root)


def _cli(root: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "hermes", "--storage", root, *args], capture_output=True, text=True
    )


def test_cli_help():
    r = subprocess.run([sys.executable, "-m", "hermes", "--help"], capture_output=True, text=True)
    assert r.returncode == 0
    for cmd in ("fetch", "inspect", "profile", "entity", "dataset"):
        assert cmd in r.stdout


def test_cli_end_to_end_against_storage(cli_storage):
    r = _cli(cli_storage, "dataset", "list")
    assert r.returncode == 0 and r.stdout.strip() == "cli_proof"

    r = _cli(cli_storage, "inspect", "cli_proof")
    assert r.returncode == 0 and "needs:" in r.stdout

    r = _cli(cli_storage, "dataset", "info", "cli_proof")
    assert r.returncode == 0 and "format: ipc" in r.stdout

    r = _cli(cli_storage, "dataset", "delete", "cli_proof")
    assert r.returncode == 0 and "deleted" in r.stdout

    r = _cli(cli_storage, "dataset", "list")
    assert r.returncode == 0 and r.stdout.strip() == ""


def test_cli_error_path(cli_storage):
    r = _cli(cli_storage, "inspect", "does_not_exist")
    assert r.returncode == 1
    assert "DatasetNotFoundError" in r.stderr


def test_cli_bad_source_exits_nonzero(cli_storage):
    r = _cli(cli_storage, "fetch", "no_such_connector")
    assert r.returncode == 1