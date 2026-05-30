# FastAPI Auth Backend

FastAPI + React 認証アプリケーションのバックエンド API です。  
FastAPI を使用した堅牢な REST API、SQLAlchemy (SQLite) によるデータ管理、JWT と bcrypt を用いたセキュアな認証機能、およびトークンブラックリストによる安全なサインアウト機能を備えています。

---

## 🛠️ 技術スタック

* **フレームワーク**: [FastAPI](https://fastapi.tiangolo.com/)
* **データベース / ORM**: SQLite / [SQLAlchemy](https://www.sqlalchemy.org/)
* **パッケージ・仮想環境管理**: [uv](https://github.com/astral-sh/uv)
* **認証**: JWT ([PyJWT](https://pyjwt.readthedocs.io/)), [bcrypt](https://github.com/pyca/bcrypt/)
* **テスト**: [pytest](https://docs.pytest.org/), [HTTPX](https://www.python-httpx.org/)

---

## 📁 ディレクトリ構成

```text
backend/
├── config.py              # Pydantic Settings を用いた環境変数・設定管理
├── database.py            # SQLAlchemy のエンジン・セッション・Baseモデル・get_db定義
├── main.py                # アプリケーションのエントリーポイント（lifespanによるテーブル自動生成等）
├── models.py              # SQLAlchemy データベースモデル (User, BlacklistedToken)
├── schemas.py             # Pydantic リクエスト/レスポンススキーマ
├── security.py            # パスワードハッシュ化・検証、JWT作成・デコード等のセキュリティ処理
├── repositories/          # データアクセスのためのリポジトリパターン層
│   ├── blacklisted_token.py
│   └── user.py
├── routers/               # ルーティングおよびエンドポイント処理
│   └── auth.py
├── tests/                 # pytest によるユニットテスト/統合テスト
│   ├── conftest.py
│   └── test_auth.py
├── pyproject.toml         # プロジェクトの依存関係とメタデータ定義
└── uv.lock                # uv のロックファイル
```

---

## 🚀 セットアップと起動方法

このプロジェクトはパッケージ管理ツールとして **`uv`** を使用しています。

### 1. 依存関係のインストール

プロジェクトのルートディレクトリ（`backend`）で以下を実行し、仮想環境の作成とパッケージのインストールを行います。

```bash
uv sync
```

### 2. 環境変数の設定

`backend/.env.example` を参考に、`backend/.env` ファイルを作成します。

```bash
cp .env.example .env
```

`.env` の中身（例）：
```ini
JWT_SECRET_KEY=change-this-secret-key-in-production  # 本番環境では安全なランダム値に変更してください
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./auth.db
```

### 3. アプリケーションの起動

開発サーバーを起動します。

```bash
uv run uvicorn main:app --reload
```

* **API サーバー**: [http://localhost:8000](http://localhost:8000)
* **インタラクティブ API ドキュメント (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **代替ドキュメント (ReDoc)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 テストの実行

`pytest` を用いて、認証関連のエンドポイントおよび処理のテストを実行できます。

```bash
# テストの実行
uv run pytest

# 詳細なログ付きでの実行
uv run pytest -v
```

---

## 🔑 主要 API エンドポイント

すべての認証系エンドポイントは `/auth` プレフィックスを持ちます。

### 1. 新規ユーザー登録 (`POST /auth/signup`)
* **説明**: 新規アカウントを登録します。パスワードは最低 8 文字以上である必要があります。
* **リクエストボディ**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
* **レスポンス (201 Created)**:
  ```json
  {
    "message": "User created successfully"
  }
  ```

### 2. サインイン (`POST /auth/signin`)
* **説明**: メールアドレスとパスワードでログインし、JWT アクセストークンを取得します。
* **リクエストボディ**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
* **レスポンス (200 OK)**:
  ```json
  {
    "access_token": "eyJhbGciOi...",
    "token_type": "bearer"
  }
  ```

### 3. サインアウト (`POST /auth/signout`)
* **説明**: 使用中の JWT トークンを無効化します（トークンをデータベースのブラックリストに登録します）。
* **ヘッダー**: `Authorization: Bearer <access_token>`
* **レスポンス (200 OK)**:
  ```json
  {
    "message": "Successfully signed out"
  }
  ```
