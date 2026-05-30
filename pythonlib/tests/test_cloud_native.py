import pytest

from camoufox.cloud_native import FileSnapshotStore, InMemoryPoolManager, SessionBroker


def test_session_broker_persists_snapshot_and_releases(tmp_path):
    broker = SessionBroker(
        snapshot_store=FileSnapshotStore(tmp_path),
        pool_manager=InMemoryPoolManager(pool_size=2),
        session_factory=lambda request: {
            "headless": True,
            "env": {
                "CAMOU_NET_PROFILE": (
                    '{"browser_family":"firefox","major_version":135,'
                    '"proxy_egress_class":"nss","transport_mode":"firefox-native"}'
                )
            },
        },
    )

    lease = broker.create_session(
        {
            "os": "windows",
            "metadata": {"tenant": "acme"},
            "ttl_seconds": 60,
        }
    )

    payload = broker.get_session(lease.session_id)
    assert payload is not None
    assert payload["snapshot"]["request"]["metadata"]["tenant"] == "acme"
    assert payload["lease"]["worker_id"].startswith("worker-")

    assert broker.release_session(lease.session_id) is True
    assert broker.get_session(lease.session_id) is None


def test_session_broker_rejects_unsafe_snapshot_key(tmp_path):
    broker = SessionBroker(
        snapshot_store=FileSnapshotStore(tmp_path),
        pool_manager=InMemoryPoolManager(pool_size=1),
        session_factory=lambda request: {"headless": True, "env": {}},
    )

    with pytest.raises(ValueError, match="snapshot_key"):
        broker.create_session({"metadata": {"snapshot_key": "../outside"}})


def test_session_broker_releases_worker_when_snapshot_save_fails(tmp_path):
    class FailingStore(FileSnapshotStore):
        def save(self, snapshot_key, payload):
            raise OSError("disk full")

    pool = InMemoryPoolManager(pool_size=1)
    broker = SessionBroker(
        snapshot_store=FailingStore(tmp_path),
        pool_manager=pool,
        session_factory=lambda request: {"headless": True, "env": {}},
    )

    with pytest.raises(OSError, match="disk full"):
        broker.create_session({})

    lease = broker.create_session.__self__.pool_manager.acquire("next", "nss")
    assert lease.active_sessions == 1
    pool.release("next")


def test_session_broker_persists_only_safe_launch_metadata(tmp_path):
    broker = SessionBroker(
        snapshot_store=FileSnapshotStore(tmp_path),
        pool_manager=InMemoryPoolManager(pool_size=1),
        session_factory=lambda request: {
            "headless": True,
            "args": ["--profile", "/tmp/secret-profile"],
            "proxy": {
                "server": "http://proxy.example:8080",
                "username": "customer-42",
                "password": "super-secret",
            },
            "env": {
                "CAMOU_CONFIG_1": '{"navigator.userAgent":"secret"}',
                "CAMOU_TLS_CIPHERS": "0x1301",
                "API_TOKEN": "secret-token",
                "DISPLAY": ":99",
            },
        },
    )

    lease = broker.create_session({"ttl_seconds": 60})
    payload = broker.get_session(lease.session_id)

    assert payload is not None
    launch = payload["snapshot"]["launch_options"]
    assert launch == {
        "args_count": 2,
        "env_keys": ["DISPLAY"],
        "headless": True,
        "proxy": {
            "server": "http://proxy.example:8080",
            "has_username": True,
            "has_password": True,
        },
    }
    serialized = str(payload["snapshot"])
    assert "super-secret" not in serialized
    assert "secret-token" not in serialized
    assert "navigator.userAgent" not in serialized
