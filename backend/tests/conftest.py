import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app
from models import User
from security import get_password_hash


@pytest.fixture()
def db_engine():
    """テストごとにクリーンなインメモリ SQLite を作成する"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()


@pytest.fixture()
def db_session(db_engine):
    """テスト用 DB セッションを返す"""
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=db_engine
    )
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session):
    """get_db をテスト用セッションで上書きした TestClient を返す"""

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def registered_user(client) -> dict:
    """サインアップ済みユーザーの認証情報を返す"""
    payload = {"email": "test@example.com", "password": "password123"}
    client.post("/auth/signup", json=payload)
    return payload


@pytest.fixture()
def auth_headers(client, registered_user) -> dict:
    """有効な Bearer トークンを含む Authorization ヘッダーを返す"""
    response = client.post("/auth/signin", json=registered_user)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def inactive_user(db_session) -> User:
    """is_active=False のユーザーを DB に作成して返す"""
    user = User(
        email="inactive@example.com",
        hashed_password=get_password_hash("password123"),
        is_active=False,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user
