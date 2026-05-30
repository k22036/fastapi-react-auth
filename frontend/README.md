# React + TypeScript + Vite Authentication Frontend

FastAPI + React 認証アプリケーションのフロントエンド SPA です。  
React 19, Vite, TypeScript, Tailwind CSS v4 を使用して構成されており、新規登録・サインイン・サインアウト機能を持つ SPA 画面を提供します。

---

## 🛠️ 技術スタック

* **ライブラリ**: [React 19](https://react.dev/)
* **ビルドツール**: [Vite 8](https://vite.dev/)
* **言語**: [TypeScript](https://www.typescriptlang.org/)
* **CSS フレームワーク**: [Tailwind CSS v4](https://tailwindcss.com/) (`@tailwindcss/vite` プラグインを使用)
* **パッケージマネージャー**: [pnpm](https://pnpm.io/)

---

## 📁 ディレクトリ構成

```text
frontend/
├── src/
│   ├── api/
│   │   └── auth.ts          # バックエンドへのAPIリクエスト処理 (fetch API)
│   ├── assets/              # 画像・アイコン等の静的アセット
│   ├── contexts/            # 認証状態管理用 React Context
│   │   ├── AuthContext.ts
│   │   └── AuthProvider.tsx
│   ├── hooks/               # カスタムフック (useAuth)
│   │   └── useAuth.ts
│   ├── pages/               # 各ページコンポーネント
│   │   ├── HomePage.tsx     # ログイン後に表示されるホーム・ダッシュボード
│   │   ├── SignInPage.tsx   # サインイン画面
│   │   └── SignUpPage.tsx   # 新規登録画面
│   ├── App.css              # アプリケーション固有のグローバルスタイル
│   ├── App.tsx              # ルーティングおよびページ切り替えのメインロジック
│   ├── index.css            # Tailwind CSS のインポートおよびベーススタイル
│   └── main.tsx             # アプリケーションのエントリーポイント
├── eslint.config.js         # ESLint 設定
├── package.json             # 依存関係とスクリプトの定義
├── tsconfig.json            # TypeScript 設定
└── vite.config.ts           # Vite 設定 (CORS 回避のためのプロキシ設定含む)
```

---

## 🔑 主要な実装・設計ポイント

### 1. 認証状態の管理 (`src/contexts/` & `src/hooks/`)
* **トークンの永続化**: サインイン成功時に取得した JWT アクセストークンは `localStorage` に保存され、ページをリロードしてもログイン状態が維持されます。
* **メールアドレスの自動デコード**: 保存されたトークン（JWT）のペイロード部分を Base64 デコードし、ユーザーのメールアドレスを自動抽出して画面に表示します。
* **カスタムフック**: コンポーネント側からは `useAuth()` を通じて、簡単に認証情報 (`isAuthenticated`, `email`, `token`) やサインアウト処理にアクセスできます。

### 2. 状態ベースの簡易ルーティング (`src/App.tsx`)
React Router などの外部ライブラリを使用せず、`isAuthenticated` のフラグおよび内部の `page` ステート (`signin` | `signup`) を用いたシンプルな条件分岐で画面を切り替えています。

### 3. 開発時の CORS 回避用プロキシ設定 (`vite.config.ts`)
ブラウザの CORS エラーを回避するため、Vite の開発サーバーのプロキシ機能を使用しています。フロントエンドから `/auth/*` へのリクエストは、自動的にバックエンドの `http://localhost:8000` へ転送されます。

---

## 🚀 開発の進め方

### 1. 依存関係のインストール

フロントエンドのルートディレクトリ（`frontend`）で以下を実行します。

```bash
pnpm install
```

### 2. 開発サーバーの起動

```bash
pnpm dev
```

起動後、 [http://localhost:5173](http://localhost:5173) にブラウザでアクセスします。  
※バックエンド API が `http://localhost:8000` で起動している必要があります。

### 3. プロダクション用ビルド

```bash
pnpm build
```

ビルドが完了すると、`dist` ディレクトリに配信用ファイルが出力されます。
