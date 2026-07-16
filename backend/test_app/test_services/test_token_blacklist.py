import pytest
from datetime import datetime, timedelta, timezone

from app.services.token_blacklist import is_token_revoked, revoke_token


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


class TestIsTokenRevoked:
    def test_returns_false_when_jti_not_blacklisted(self, fake_redis):
        payload = {"jti": "token-1"}
        assert is_token_revoked(payload) is False

    def test_returns_true_when_jti_blacklisted(self, fake_redis):
        fake_redis.set("bl:jti:token-2", "1", ex=300)
        payload = {"jti": "token-2"}
        assert is_token_revoked(payload) is True

    def test_returns_true_when_jti_missing(self, fake_redis):
        payload = {}
        assert is_token_revoked(payload) is True


class TestRevokeToken:
    def test_sets_blacklist_key_with_positive_ttl(self, fake_redis):
        future_exp = int(
            (datetime.now(timezone.utc) + timedelta(minutes=5)).timestamp()
        )
        payload = {"jti": "token-3", "exp": future_exp}

        revoke_token(payload)

        assert fake_redis.exists("bl:jti:token-3") == 1
        assert fake_redis.last_set_call is not None
        key, value, ex = fake_redis.last_set_call
        assert key == "bl:jti:token-3"
        assert value == "1"
        assert ex is not None and ex > 0

    def test_does_not_set_key_when_token_expired(self, fake_redis):
        past_exp = int((datetime.now(timezone.utc) - timedelta(minutes=1)).timestamp())
        payload = {"jti": "token-4", "exp": past_exp}

        revoke_token(payload)

        assert fake_redis.exists("bl:jti:token-4") == 0

    @pytest.mark.parametrize(
        "payload",
        [
            {
                "exp": int(
                    (datetime.now(timezone.utc) + timedelta(minutes=5)).timestamp()
                )
            },  # missing jti
            {"jti": "token-5"},  # missing exp
            {},  # missing both
        ],
    )
    def test_noop_when_required_claims_missing(self, fake_redis, payload):
        revoke_token(payload)
        # no call should be made to set the key in Redis since either jti or exp is missing
        assert fake_redis.last_set_call is None
