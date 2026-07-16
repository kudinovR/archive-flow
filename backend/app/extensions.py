from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import redis

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()


class RedisClient:
    client = None


redis_client = RedisClient()


def init_redis(app):
    redis_client.client = redis.Redis.from_url(
        app.config["REDIS_URL"],
        decode_responses=True,
    )
    try:
        redis_client.client.ping()
        app.logger.info("Redis connection established")
    except redis.RedisError as exc:
        app.logger.warning(f"Redis unavailable at startup: {exc}")
