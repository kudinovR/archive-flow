from datetime import datetime, timezone
from typing import Any

from app.extensions import redis_client


def _blacklist_key(jti: str) -> str:
    return f"bl:jti:{jti}"


def is_token_revoked(jwt_payload: dict[str, Any]) -> bool:
    jti = jwt_payload.get("jti")
    if not jti:
        return True  # secure by default

    key = _blacklist_key(jti)
    return redis_client.client.exists(key) == 1


def revoke_token(jwt_payload: dict[str, Any]) -> None:
    """
    Adds token JTI to Redis blacklist with TTL equal to remaining token lifetime.
    Safe no-op if token is already expired or required claims are missing.
    """
    jti = jwt_payload.get("jti")
    exp = jwt_payload.get("exp")
    if not jti or not exp:
        return

    now_ts = int(datetime.now(timezone.utc).timestamp())
    ttl = int(exp) - now_ts
    if ttl <= 0:
        return

    redis_client.client.set(_blacklist_key(jti), "1", ex=ttl)
