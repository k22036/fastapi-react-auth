"""
auth エンドポイントのテスト

テスト対象:
  POST /auth/signup  - 新規ユーザー登録
  POST /auth/signin  - サインイン（JWT 取得）
  POST /auth/signout - サインアウト（トークン無効化）
"""

from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from security import create_access_token

# ---------------------------------------------------------------------------
# POST /auth/signup
# ---------------------------------------------------------------------------


class TestSignUp:
    def test_success(self, client: TestClient):
        """正常系: 新規ユーザーを登録できる"""
        response = client.post(
            "/auth/signup",
            json={"email": "new@example.com", "password": "password123"},
        )
        assert response.status_code == 201
        assert response.json() == {"message": "User created successfully"}

    def test_duplicate_email_returns_409(
        self, client: TestClient, registered_user: dict
    ):
        """異常系: 同じメールアドレスで再登録すると 409"""
        response = client.post("/auth/signup", json=registered_user)
        assert response.status_code == 409
        assert "already registered" in response.json()["detail"]

    def test_invalid_email_format_returns_422(self, client: TestClient):
        """異常系: 不正なメールアドレス形式は 422"""
        response = client.post(
            "/auth/signup",
            json={"email": "not-an-email", "password": "password123"},
        )
        assert response.status_code == 422

    def test_password_too_short_returns_422(self, client: TestClient):
        """異常系: パスワードが 8 文字未満は 422"""
        response = client.post(
            "/auth/signup",
            json={"email": "test@example.com", "password": "short"},
        )
        assert response.status_code == 422

    def test_missing_email_returns_422(self, client: TestClient):
        """異常系: email フィールドが欠落すると 422"""
        response = client.post(
            "/auth/signup", json={"password": "password123"})
        assert response.status_code == 422

    def test_missing_password_returns_422(self, client: TestClient):
        """異常系: password フィールドが欠落すると 422"""
        response = client.post(
            "/auth/signup", json={"email": "test@example.com"})
        assert response.status_code == 422

    def test_empty_body_returns_422(self, client: TestClient):
        """異常系: ボディが空のリクエストは 422"""
        response = client.post("/auth/signup", json={})
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# POST /auth/signin
# ---------------------------------------------------------------------------


class TestSignIn:
    def test_success_returns_token(self, client: TestClient, registered_user: dict):
        """正常系: 正しい認証情報で JWT トークンが返る"""
        response = client.post("/auth/signin", json=registered_user)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0

    def test_wrong_password_returns_401(
        self, client: TestClient, registered_user: dict
    ):
        """異常系: パスワードが間違っていると 401"""
        response = client.post(
            "/auth/signin",
            json={"email": registered_user["email"],
                  "password": "wrongpassword"},
        )
        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]

    def test_nonexistent_email_returns_401(self, client: TestClient):
        """異常系: 存在しないメールアドレスは 401"""
        response = client.post(
            "/auth/signin",
            json={"email": "nobody@example.com", "password": "password123"},
        )
        assert response.status_code == 401

    def test_invalid_email_format_returns_422(self, client: TestClient):
        """異常系: 不正なメールアドレス形式は 422"""
        response = client.post(
            "/auth/signin",
            json={"email": "notanemail", "password": "password123"},
        )
        assert response.status_code == 422

    def test_inactive_user_returns_403(self, client: TestClient, db_session):
        """異常系: 無効化されたアカウントでサインインすると 403"""
        from models import User
        from security import get_password_hash

        user = User(
            email="inactive@example.com",
            hashed_password=get_password_hash("password123"),
            is_active=False,
        )
        db_session.add(user)
        db_session.commit()

        response = client.post(
            "/auth/signin",
            json={"email": "inactive@example.com", "password": "password123"},
        )
        assert response.status_code == 403
        assert "inactive" in response.json()["detail"].lower()


# ---------------------------------------------------------------------------
# POST /auth/signout
# ---------------------------------------------------------------------------


class TestSignOut:
    def test_success(self, client: TestClient, auth_headers: dict):
        """正常系: 有効なトークンでサインアウトできる"""
        response = client.post("/auth/signout", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == {"message": "Successfully signed out"}

    def test_token_already_invalidated_returns_401(
        self, client: TestClient, auth_headers: dict
    ):
        """異常系: 同じトークンで 2 回サインアウトすると 401"""
        client.post("/auth/signout", headers=auth_headers)
        response = client.post("/auth/signout", headers=auth_headers)
        assert response.status_code == 401
        assert "already been invalidated" in response.json()["detail"]

    def test_invalid_token_returns_401(self, client: TestClient):
        """異常系: 不正なトークンは 401"""
        response = client.post(
            "/auth/signout",
            headers={"Authorization": "Bearer this.is.not.a.valid.token"},
        )
        assert response.status_code == 401

    def test_no_authorization_header_returns_401(self, client: TestClient):
        """異常系: Authorization ヘッダーがない場合は 401"""
        response = client.post("/auth/signout")
        assert response.status_code == 401

    def test_expired_token_returns_401(self, client: TestClient):
        """異常系: 期限切れトークンは 401"""
        expired_token = create_access_token(
            subject="test@example.com",
            expires_delta=timedelta(hours=-1),
        )
        response = client.post(
            "/auth/signout",
            headers={"Authorization": f"Bearer {expired_token}"},
        )
        assert response.status_code == 401
        assert "expired" in response.json()["detail"].lower()

    def test_signin_after_signout_succeeds(
        self, client: TestClient, registered_user: dict, auth_headers: dict
    ):
        """正常系: サインアウト後も再サインインに成功する"""
        client.post("/auth/signout", headers=auth_headers)

        response = client.post("/auth/signin", json=registered_user)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
