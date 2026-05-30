# FastAPI + React Authentication App

FastAPI バックエンドと React フロントエンドで構成された、ユーザー認証機能（サインアップ、サインイン、サインアウト）のフルスタックアプリケーションです。

---

## 📁 プロジェクト構成

本リポジトリは、以下のモノレポ構成となっています。

* **[backend/](backend)**:
  * FastAPI、SQLAlchemy (SQLite)、JWT、bcrypt を用いたセキュアな認証 API。
  * 詳細は [backend/README.md](backend/README.md) を参照してください。
* **[frontend/](frontend)**:
  * React 19、Vite 8、TypeScript、Tailwind CSS v4 を用いた SPA。
  * 詳細は [frontend/README.md](frontend/README.md) を参照してください。

---

## 🚀 クイックスタート

開発環境でアプリケーション全体を起動する手順です。

### 前提条件

* Python 3.13 以上
* [uv](https://github.com/astral-sh/uv) (バックエンドの管理用)
* Node.js 20 以上
* [pnpm](https://pnpm.io/) (フロントエンドの管理用)

---

### 1. バックエンドの起動

1. バックエンドディレクトリに移動します。

   ```bash
   cd backend
   ```

2. 依存関係のセットアップと環境変数の設定を行います。

   ```bash
   uv sync
   cp .env.example .env
   ```

3. 開発用 API サーバーを起動します。

   ```bash
   uv run uvicorn main:app --reload
   ```

   API サーバーは [http://localhost:8000](http://localhost:8000) で起動します。また、[http://localhost:8000/docs](http://localhost:8000/docs) から Swagger UI ドキュメントを表示できます。

---

### 2. フロントエンドの起動

別のターミナルセッションを開き、以下の手順を実行します。

1. フロントエンドディレクトリに移動します。

   ```bash
   cd frontend
   ```

2. 依存関係をインストールします。

   ```bash
   pnpm install
   ```

3. 開発用サーバーを起動します。

   ```bash
   pnpm dev
   ```

   フロントエンドは [http://localhost:5173](http://localhost:5173) で起動します。

---

## 🔌 開発時の通信について

フロントエンドからバックエンド API への接続は、Vite の開発サーバープロキシ機能によって自動転送されます。  
フロントエンド側の `/auth/*` への API リクエストは、自動的に `http://localhost:8000/auth/*` へ転送されるため、開発時に CORS のエラーを回避できます（設定の詳細は [vite.config.ts](frontend/vite.config.ts) を参照）。
