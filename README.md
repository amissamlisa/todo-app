# Todo App

目標達成を支援する Web アプリです。FastAPI + React + PostgreSQL で構成し、OpenAI API を使って目標タスクを自動生成できます。

この README は、個人開発を前提に「AWS 運用を主軸」にしつつ、「将来の自分のためのローカル復旧手順」を最小限残す方針で整理しています。

## 技術スタック

- Backend: FastAPI, SQLAlchemy, Alembic, Poetry
- Frontend: React, TypeScript, Vite, Tailwind CSS
- Database: PostgreSQL
- Infrastructure (local): Docker Compose
- AI: OpenAI Responses API

## 実装済み機能

- 認証: 登録、ログイン、ログアウト、トークン更新、パスワードリセット
- 目標管理: 目標の作成、更新、削除、ステータス更新
- 目標タスク管理: 作成、更新、削除、並び替え、ステータス更新
- トップ画面: ユーザー情報 + 現在の目標 + タスク一覧
- AIタスク生成: 目標と可用時間からタスク候補を生成

## ディレクトリ

```text
todo-app/
├─ backend/
├─ frontend/
├─ docker-compose.yml
└─ .env.example
```

## AWS 運用向けメモ（個人開発向け）

このリポジトリはローカルでのコンテナ実行を基準にしています。AWS へ上げる際は次を最初に決めるのが安全です。

1. コンテナ実行基盤（ECS/Fargate など）
2. DB 配置（RDS for PostgreSQL など）
3. シークレット管理（Secrets Manager / SSM Parameter Store）
4. API と Frontend の公開経路（ALB + ドメイン + TLS）
5. CI/CD のデプロイ単位（backend/frontend を分離するか）

注意点:

- [docker-compose.yml](docker-compose.yml) のデフォルト値はローカル向けです。
- 本番では環境変数のデフォルト値に依存しないでください。
- 秘密情報は Git 管理しないでください。

## 環境変数

サンプルは [.env.example](.env.example) を参照してください。実値はルートの `.env` に置き、Git へコミットしません。

主な変数:

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `JWT_SECRET_KEY`
- `PASSWORD_RESET_URL`
- `RESEND_API_KEY`
- `OPENAI_API_KEY`

補足:

- Backend の `SQLALCHEMY_DATABASE_URL` は [docker-compose.yml](docker-compose.yml) で組み立てています。
- Frontend ローカル実行時は `frontend/.env` に `VITE_API_BASE_URL` が必要です。

## ローカル最短復旧手順

AWS 運用が主でも、障害切り分けと将来の再開用にこの手順だけ残しています。

1. `.env` を作成（例: `.env.example` をコピー）
2. 起動

```bash
docker compose up -d --build
```

3. 確認

```bash
docker compose ps
```

4. 参照先

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Swagger: http://localhost:8000/docs

停止:

```bash
docker compose down
```

## 開発コマンド

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

## マイグレーション

```bash
cd backend
alembic upgrade head
```

Alembic は [backend/alembic/env.py](backend/alembic/env.py) で接続先を決定します。

- `ALEMBIC_DATABASE_URL` があればそれを使用
- それ以外は `SQLALCHEMY_DATABASE_URL` などを参照

## テスト

```bash
cd backend
python -m pytest test
```

テストコードは [backend/test/test_setup.py](backend/test/test_setup.py) の DB 接続環境変数を参照します。

- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`

## API エンドポイント（抜粋）

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

## セキュリティ

- 秘密情報は `.env` に置き、絶対に Git にコミットしない
- 誤って漏えいした場合は、鍵やパスワードを即ローテーションする
- AWS 本番では Secrets Manager などの利用を推奨
