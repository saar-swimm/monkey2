from unittest.mock import MagicMock

import pytest

from infection_monkey.credential_collectors import SSHCredentialCollector, SSHKeypair, Username
from infection_monkey.i_puppet.credential_collection import Credentials


@pytest.fixture
def patch_telemetry_messenger():
    return MagicMock()


def patch_ssh_handler(ssh_creds, monkeypatch):
    monkeypatch.setattr(
        "infection_monkey.credential_collectors.ssh_collector.ssh_handler.get_ssh_info",
        lambda _: ssh_creds,
    )


@pytest.mark.parametrize(
    "ssh_creds", [([{"name": "", "home_dir": "", "public_key": None, "private_key": None}]), ([])]
)
def test_ssh_credentials_empty_results(monkeypatch, ssh_creds, patch_telemetry_messenger):
    patch_ssh_handler(ssh_creds, monkeypatch)
    collected = SSHCredentialCollector(patch_telemetry_messenger).collect_credentials()
    assert not collected


def test_ssh_info_result_parsing(monkeypatch, patch_telemetry_messenger):

    ssh_creds = [
        {
            "name": "ubuntu",
            "home_dir": "/home/ubuntu",
            "public_key": "SomePublicKeyUbuntu",
            "private_key": "ExtremelyGoodPrivateKey",
        },
        {
            "name": "mcus",
            "home_dir": "/home/mcus",
            "public_key": "AnotherPublicKey",
            "private_key": None,
        },
        {"name": "guest", "home_dir": "/", "public_key": None, "private_key": None},
    ]
    patch_ssh_handler(ssh_creds, monkeypatch)

    # Expected credentials
    username = Username("ubuntu")
    username2 = Username("mcus")
    username3 = Username("guest")

    ssh_keypair1 = SSHKeypair("ExtremelyGoodPrivateKey", "SomePublicKeyUbuntu")
    ssh_keypair2 = SSHKeypair("", "AnotherPublicKey")

    expected = [
        Credentials(identities=[username], secrets=[ssh_keypair1]),
        Credentials(identities=[username2], secrets=[ssh_keypair2]),
        Credentials(identities=[username3], secrets=[]),
    ]
    collected = SSHCredentialCollector(patch_telemetry_messenger).collect_credentials()
    assert expected == collected
