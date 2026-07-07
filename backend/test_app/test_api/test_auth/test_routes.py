import pytest


API_REGISTER = "/api/auth/register"
API_LOGIN = "/api/auth/login"
DEFAULT_PASSWORD = "password123"


class TestRegister:
    def test_register_success(self, client, user_payload):
        res = client.post(API_REGISTER, json=user_payload())
        assert res.status_code == 201
        data = res.get_json()
        assert "id" in data
        assert data["message"] == "User registered successfully"

    @pytest.mark.parametrize(
        "payload",
        [
            {"password": DEFAULT_PASSWORD},
            {"email": "a@example.com"},
            {},
        ],
    )
    def test_register_invalid_payload(self, client, payload):
        res = client.post(API_REGISTER, json=payload)
        assert res.status_code == 400
        assert "error" in res.get_json()

    def test_register_duplicate_email_case_insensitive(self, client, user_payload):
        first_payload = user_payload(
            email="Case@Test.com",
            password=DEFAULT_PASSWORD,
        )
        second_payload = user_payload(
            email="case@test.com",
            password=DEFAULT_PASSWORD,
        )

        client.post(API_REGISTER, json=first_payload)
        res = client.post(API_REGISTER, json=second_payload)
        assert res.status_code == 409
        assert "error" in res.get_json()

    def test_register_email_normalized(self, client):
        res = client.post(
            API_REGISTER,
            json={"email": "  UPPER@EXAMPLE.COM  ", "password": DEFAULT_PASSWORD},
        )
        assert res.status_code == 201


class TestLogin:
    def test_login_success(self, client, user_payload):
        payload = user_payload()
        client.post(API_REGISTER, json=payload)
        res = client.post(API_LOGIN, json=payload)

        assert res.status_code == 200
        data = res.get_json()
        assert "access_token" in data
        assert data.get("role") == "user"

    def test_login_missing_password_returns_400(self, client):
        res = client.post(API_LOGIN, json={"email": "a@example.com"})
        assert res.status_code == 400
        assert res.get_json()["error"] == "Email and password are required"

    def test_login_unknown_user_returns_401(self, client):
        res = client.post(
            API_LOGIN,
            json={"email": "nobody@example.com", "password": DEFAULT_PASSWORD},
        )
        assert res.status_code == 401
        assert res.get_json()["error"] == "Invalid email or password"

    def test_login_same_error_for_wrong_email_and_wrong_password(
        self, client, user_payload
    ):
        payload = user_payload(email="enum@example.com")
        client.post(API_REGISTER, json=payload)

        res_wrong_pass = client.post(
            API_LOGIN, json={"email": payload["email"], "password": "wrong"}
        )
        res_wrong_email = client.post(
            API_LOGIN,
            json={"email": "noexist@example.com", "password": DEFAULT_PASSWORD},
        )

        assert res_wrong_pass.status_code == 401
        assert res_wrong_email.status_code == 401
        assert res_wrong_pass.get_json()["error"] == res_wrong_email.get_json()["error"]
