import pytest
from app.services.auth_service import register_user, login_user
from app.models import User


@pytest.fixture
def app_ctx(app):
    with app.app_context():
        yield


class TestRegisterUser:
    def test_returns_201_on_success(self, app_ctx, user_payload):
        result, status = register_user(user_payload())
        assert status == 201
        assert "id" in result

    @pytest.mark.parametrize(
        "payload",
        [
            {"password": "pass123"},
            {"email": "svc@example.com"},
            {},
        ],
    )
    def test_returns_400_for_invalid_payload(self, app_ctx, payload):
        _, status = register_user(payload)
        assert status == 400

    def test_returns_409_on_duplicate_case_insensitive(self, app_ctx):
        register_user({"email": "DUP@EXAMPLE.COM", "password": "pass123"})
        _, status = register_user({"email": "dup@example.com", "password": "pass123"})
        assert status == 409

    def test_password_is_hashed(self, app_ctx):
        register_user({"email": "hash@example.com", "password": "plaintext"})
        user = User.query.filter_by(email="hash@example.com").first()
        assert user.password_hash != "plaintext"
        assert user.password_hash.startswith("$argon2")

    def test_email_stored_lowercase(self, app_ctx):
        register_user({"email": "  CAPS@Test.COM  ", "password": "pass123"})
        user = User.query.filter_by(email="caps@test.com").first()
        assert user is not None


class TestLoginUser:
    def test_returns_200_with_token(self, app_ctx):
        register_user({"email": "lgn@example.com", "password": "pass123"})
        result, status = login_user({"email": "lgn@example.com", "password": "pass123"})
        assert status == 200
        assert "access_token" in result
        assert result["role"] == "user"

    def test_returns_401_wrong_password(self, app_ctx):
        register_user({"email": "lgn2@example.com", "password": "correct"})
        _, status = login_user({"email": "lgn2@example.com", "password": "wrong"})
        assert status == 401

    def test_returns_401_unknown_email(self, app_ctx):
        _, status = login_user({"email": "ghost@example.com", "password": "pass"})
        assert status == 401

    @pytest.mark.parametrize(
        "payload",
        [
            {"email": "lgn3@example.com"},
            {"password": "pass123"},
            {},
        ],
    )
    def test_returns_400_missing_fields(self, app_ctx, payload):
        _, status = login_user(payload)
        assert status == 400
