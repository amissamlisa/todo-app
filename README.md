# Todo App

目標達成を支援する Web アプリケーションです。大きな目標を入力すると、現在の状況や使える時間をもとに、達成までのタスクを分解して日々の進捗を管理できます。

アプリケーション URL: https://claidy-todo.com

## 概要

このアプリは、「やりたいことはあるが、何から着手すればいいかわからない」という課題を解消することを目的に開発しました。

ユーザーは達成したい目標、現状、開始日、期限日、平日・休日に使える時間などを入力します。すると、AI が条件に応じた現実的なタスク案を生成し、ユーザーはそのタスクを調整しながら日々の進捗を追跡できます。
目標タスクを1週間ごとに設定して完了後、その都度タスクを更新できます。

## 主な機能

- ユーザー登録、ログイン、ログアウト
- JWTとHttpOnly Cookieを使った認証管理
- パスワードリセットメール送信と再設定
- 目標の登録、更新、削除、達成ステータス変更
- AI による目標達成タスクの自動生成
- タスクの手動登録、更新、削除
- タスクの順序変更、進捗ステータス変更
- トップ画面での目標・タスク一覧確認

## 利用フロー

1. ユーザー登録またはログインを行う
2. 達成したい目標、現在の状況、開始日、期限日、使える時間を入力する
3. AI に目標達成タスクを生成させる
4. 生成されたタスクを必要に応じて手動で調整する
5. トップ画面から日々の進捗を更新する
6. ポイントに応じてランクが上がる

## 機能要件

- 目標に対して未達成のアクティブな計画を1件管理できること
- 目標に紐づくタスクを一覧・追加・編集・削除できること
- タスクの並び順と進捗状態を更新できること
- パスワードリセットをメール経由で行えること
- AI 生成結果をそのまま使うだけでなく、後から手動で修正できること
- 主要ブラウザで利用できること

## 非機能要件
- フォーム入力やタスク更新がスムーズに行えること
- 認証、CORS、Cookie 設定を適切に扱い、典型的な脆弱性を避けること

## 使用技術

### Frontend
- TypeScript 5.9
- React 19.2
- Vite 7.2
- React Hook Form
- Axios
- Day.js
- Tailwind CSS

### Backend
- Python 3.13
- FastAPI 0.115
- SQLAlchemy 2.x
- Alembic
- Pydantic v2
- PostgreSQL
- OpenAI API
- Resend API

### CI/CD・Deploy
- GitHub Actions
- Docker Compose
- EC2
- Route53

## 選定理由

### Frontend
TypeScript を選定した理由は、フォーム入力や API レスポンスなど、フロントエンドで扱うデータ構造が多いためです。型を明示することで、画面実装時の安全性と可読性を高めやすくなります。

React を選定した理由は、画面状態の変化に応じて UI を柔軟に更新しやすいためです。本アプリでは認証状態、目標入力フォーム、タスク編集モーダル、一覧表示など状態変化の多い画面が中心であり、コンポーネント指向との相性が良いと判断しました。

### Backend

FastAPI を選定した理由は、型ヒントを活かした API 開発がしやすく、フロントエンド分離型の構成と相性が良いためです。バリデーション、レスポンス定義、OpenAPI 生成まで一貫して扱える点も大きな利点でした。

PostgreSQL を選定した理由は、目標、タスク、ユーザー、トークンといった永続化データを安全に扱う必要があったためです。ORM とマイグレーションを組み合わせることで、開発速度と保守性の両立を狙っています。

### インフラ
ローカル開発は Docker Compose を利用し、Frontend、Backend、PostgreSQL をまとめて起動できるようにしています。本番は EC2 上で Docker Compose を実行し、GitHub Actions から SSH でデプロイする構成です。ドメイン管理には Route53 を利用しています。

## 設計

### アーキテクチャ

全体としては、Frontend、Backend、Database を分離した構成です。
- Frontend は `features` と `shared` に分かれており、認証やタスク操作などの画面ロジックを機能単位で整理しています
- Backend は `routers`、`schemas`、`models`、`repository` に責務を分離しています
- DB アクセスは repository 層に寄せ、ルーター側ではユースケース処理に集中しやすい形にしています

### バックエンド設計のポイント

- `routers` でエンドポイントごとの責務を分離
- `schemas` でリクエスト/レスポンスの型とバリデーションを管理
- `models` で SQLAlchemy モデルを定義
- `repository` で DB 操作を集約
- `exception_handler` で例外レスポンスを統一

### フロントエンド設計のポイント

- `features/tasks` と `features/users` に機能を分離
- `shared/components` に再利用 UI を集約
- `react-hook-form` を使ってフォームバリデーションを統一
- 認証や API 呼び出しを Hook / Provider に分離して見通しを保つ

## 工夫した点

### 1. AI タスク生成をアプリの中心機能にしたこと
単にAIへ自由入力を渡すのではなく、目標、現状、期限、可用時間、追加条件を構造化して渡すことで、実行可能性の高いタスク案を生成できるようにしています。

### 2. 認証とパスワードリセットを分離フロントエンド構成で実装したこと
CookieとCORS の扱いを含めて、SPA + API 構成でも安全に認証できるよう調整しています。パスワードリセットではメール送信、トークン検証、再設定の流れを分離して実装しています。

## ディレクトリ構成

```text
todo-app/
├─ backend/
│  ├─ routers/
│  ├─ models/
│  ├─ schemas/
│  ├─ repository/
│  └─ test/
├─ frontend/
│  └─ src/
│     ├─ features/
│     └─ shared/
├─ docker-compose.yml
└─ .env.example
```

## ローカル開発

### 環境変数

サンプルは [.env.example](.env.example) を参照してください。実値はルートの `.env` に置き、Git へコミットしません。

主に使用する変数:

- `JWT_SECRET_KEY`
- `OPENAI_API_KEY`
- `SQLALCHEMY_DATABASE_URL`
- `RESEND_API_KEY`
- `PASSWORD_RESET_URL`
- `ALLOWED_ORIGIN_URL`
- `COOKIE_SECURE`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`

### 起動方法

```bash
docker compose up -d --build
```



本番環境の参照先:

- Frontend: https://claidy-todo.com
- Backend API: https://claidy-todo.com/api

停止:

```bash
docker compose down
```

### 個別起動

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Backend:

```bash
cd backend
poetry install
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```



CI では Frontend の lint / build と Backend の compile check / pytest を GitHub Actions で実行しています。

## API エンドポイント（抜粋）
実装上、同一エンドポイントは `/<path>` と `/api/<path>` の両方で利用できます。

Auth:

- `POST /auth/registration`
- `POST /auth/login`
- `DELETE /auth/logout`
- `POST /auth/refresh`
- `POST /auth/password-reset/request`
- `GET /auth/password-reset/verification`
- `PUT /auth/password-reset`

Goals:

- `POST /goal/`
- `PUT /goal/`
- `GET /goal/{goal_id}`
- `PATCH /goal/{goal_id}`
- `DELETE /goal/{goal_id}`

Goal Tasks:

- `GET /goal-tasks/{goal_id}`
- `POST /goal-tasks/generate`
- `POST /goal-tasks`
- `PUT /goal-tasks/order`
- `PUT /goal-tasks/status/{goal_task_id}`
- `PUT /goal-tasks/{goal_task_id}`
- `DELETE /goal-tasks/{goal_task_id}`

Top / Users:

- `GET /top/`
- `PUT /users/points`
- `PUT /users/rank`
