import os
import shutil
from uuid import uuid4

import pytest
from app import create_app
from app.extensions import db as _db
from app.models import User


class FakeRedis:
    def __init__(self):
        self._keys = set()
        self.last_set_call = None

    def exists(self, key: str) -> int:
        return 1 if key in self._keys else 0

    def set(self, key: str, value: str, ex: int | None = None) -> bool:
        # Mimic Redis SET with expiry: only persist keys when a positive TTL is provided.
        self.last_set_call = (key, value, ex)
        if ex is not None and ex > 0:
            self._keys.add(key)
            return True
        return False


@pytest.fixture
def fake_redis(monkeypatch):
    from app.services import token_blacklist

    fake = FakeRedis()
    monkeypatch.setattr(token_blacklist.redis_client, "client", fake)
    return fake


@pytest.fixture(scope="session")
def app():
    app = create_app("testing")

    # Guard: Ensure that the test config is actually active
    assert app.config["TESTING"] is True
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"

    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_db(app):

    # Test isolation despite session-scoped app
    with app.app_context():
        _db.session.query(User).delete()
        _db.session.commit()
    yield


@pytest.fixture
def user_payload():
    # Unique test data per call
    def _make(email=None, password="testpassword123"):
        email = email or f"test-{uuid4().hex[:8]}@example.com"
        return {"email": email, "password": password}

    return _make


@pytest.fixture
def auth_headers(client, user_payload):
    payload = user_payload()
    client.post("/api/auth/register", json=payload)
    res = client.post("/api/auth/login", json=payload)
    token = res.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="session", autouse=True)
def ensure_test_upload_dir(app):
    upload_dir = app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_dir, exist_ok=True)
    yield
    shutil.rmtree(upload_dir, ignore_errors=True)
