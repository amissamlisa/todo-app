# Todo App

目標達成を支援する Web アプリケーションです。大きな目標を入力すると、現在の状況や使える時間をもとに、達成までのタスクを分解して日々の進捗を管理できます。

**アプリケーションURL**: https://claidy-todo.com

## 目次

- [概要](#概要)
- [主な機能](#主な機能)
- [利用フロー](#利用フロー)
- [機能要件](#機能要件)
- [非機能要件](#非機能要件)
- [デザイン](#デザイン)
- [使用技術](#使用技術)
- [選定理由](#選定理由)
- [設計](#設計)
- [工夫した点](#工夫した点)
- [ディレクトリ構成](#ディレクトリ構成)
- [ローカル開発](#ローカル開発)
- [API エンドポイント（抜粋）](#api-エンドポイント抜粋)


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
- スマートフォンで利用できること

## 非機能要件

- フォーム入力やタスク更新がスムーズに行えること
- 認証、CORS、Cookie 設定を適切に扱い、典型的な脆弱性を避けること

## デザイン

- Figma Prototype: https://www.figma.com/proto/jWEf04IynZWLrwvzhZQtb8/Claidy-Todo?node-id=1-3&t=YjcooF2KQCfe325v-1&scaling=scale-down&content-scaling=fixed&page-id=0%3A1
- Figma File: https://www.figma.com/design/jWEf04IynZWLrwvzhZQtb8/Claidy-Todo?node-id=0-1&t=uVRIQqSKeU2TuNQt-1
- 設計図（ユースケース図・状態遷移図・アクティビティ図・ドメイン図・オブジェクト図）: https://drive.google.com/file/d/1XKa1Pl9Nu5QRXsCnu_sK4qrYXYZmYLco/view?usp=sharing
- ER図（Users / Goals / GoalsTasks / RefreshTokens / PasswordResetTokens）: https://drive.google.com/file/d/1c49YS8oJzUWTIPuK2JfK4ZBm9OnT3jLk/view?usp=sharing
- クラス図（Repository / Model / Enum）: https://drive.google.com/file/d/184z2NkowI4c-oqmsy0K-cYI0V7opyf43/view?usp=sharing
- 画面遷移図: https://drive.google.com/file/d/11UmfgC_1m-QQazRRAIn-nro6V8UU4eW1/view?usp=sharing


## 使用技術

### Frontend
- TypeScript 5.9.3
- React 19.2.0
- React Router DOM 7.10.1
- Vite 7.2.4
- React Hook Form 7.69.0
- Axios 1.13.2
- Day.js 1.11.20
- Tailwind CSS 4.1.18

### Backend
- Python 3.13（runtime: python:3.13-slim / pyproject: >=3.13,<3.14）
- FastAPI 0.115.0
- Uvicorn 0.30.0
- SQLAlchemy 2.x（>=2.0,<3.0）
- Alembic 1.13.0
- Pydantic 2.x（>=2.7,<3.0）
- PostgreSQL 16.2
- OpenAI Python SDK 1.x（>=1.0,<2.0）
- Resend API

### CI/CD・Deploy
- GitHub Actions
- Docker Compose
- EC2
- Route53

## 選定理由

### フロントエンド
#### TypeScript 
TypeScriptは静的型付けにより、実行前に型の不整合を検出できるため採用しました。 

本アプリでは、バックエンドとのAPI通信時にレスポンス型やリクエスト型を定義し、フロントエンド側のデータ構造との整合性を保っています。  

また、認証情報やフォーム入力、UI状態の管理にも型を活用しており、想定外の値や実装ミスを早期に発見できる構成としています。  

さらに、Propsや関数引数の型を明示することで、機能追加や仕様変更時にも影響範囲を把握しやすく、保守性の向上につながると考えました。

#### React
個人開発では新しい技術にも挑戦し、フロントエンド開発の知見を広げたいと考え、Reactを採用しました。

本アプリはログイン、ユーザー登録、パスワード再設定、目標管理、タスク管理など複数の画面で構成されるSPAです。そのため、React Routerを利用した画面遷移管理との相性が良いと考えました。

また、ログインやタスク作成・更新などフォームを扱う機能が多いため、React Hook Formを活用することでフォーム管理を効率的に行えると判断しました。

さらに、認証状態やKanbanボード、モーダル表示など状態変化の多いUIを扱うため、コンポーネントとHooksを活用して責務を分離し、保守性や拡張性の高い実装ができると考えました。

### バックエンド

#### FastAPI
FastAPIを採用した理由は、Reactと連携するSPA向けのAPIサーバーを効率的に構築できるためです。

本アプリではフロントエンドとバックエンドを分離した構成を採用しており、認証や目標管理、タスク管理などの機能をREST APIとして提供しています。

また、Pydanticによる型安全なバリデーションを利用することで、会員登録や目標・タスク作成時の入力検証をAPI境界で一元管理しています。これにより、不正なリクエストを早期に検知し、安定したAPIを提供できると考えました。

さらに、Swagger/OpenAPIによるAPIドキュメントを自動生成できるため、API仕様の確認やフロントエンドとの連携を効率的に行える点も採用理由です。

### OpenAI API
本アプリの中核機能である「目標からタスクを生成する機能」を実現するために採用しました。

ユーザーごとに目標や期限、利用可能時間が異なるため、生成AIを利用して柔軟にタスクを提案できるようにしています。

### PostgreSQL
PostgreSQLを選んだ理由は、ユーザー・目標・タスクなど関連性のあるデータを扱うためRDBMSが適していると考えたためです。

実際にForeignKeyによる参照整合性やCheckConstraintによる制約を利用し、アプリケーションだけでなくDBレベルでもデータ品質を担保しています。

また、今回の個人開発ではPostgreSQLに興味があり、今後の技術選定の判断材料にするため実際に採用して学習しました。

### Docker Compose
フロントエンド、バックエンド、データベースを一括管理し、開発環境と本番環境の差異を小さくするため採用しました。

### AWS EC2
小規模な個人開発でも運用コストを抑えられ、Docker Composeによるコンテナ運用との相性が良いと考え採用しました。

### Route53
独自ドメインによるWebサイト公開や、Resendを利用したメール送信時のドメイン認証（SPF/DKIM）を管理するため採用しました。

### Nginx
Nginxを採用した理由は、Reactの静的ファイル配信、FastAPIへのリバースプロキシ、HTTPS化を1台のEC2上で実現できるためです。また、ロードバランサーなどのマネージドサービスを利用せずに構築できるため、個人開発における運用コストを抑えられる点も考慮しました。

### Resend
当初はAmazon SESの利用を検討しましたが、個人開発環境では審査や設定のハードルが高く、開発速度を優先するためResendへ切り替えました。
APIがシンプルでFastAPIとの連携も容易だったため採用しました。

### インフラ
ローカル開発は Docker Compose を利用し、Frontend、Backend、PostgreSQL をまとめて起動できるようにしています。本番は EC2 上で Docker Compose を実行し、GitHub Actions から SSH でデプロイする構成です。ドメイン管理には Route53 を利用しています。

## 設計

### アーキテクチャ

全体としては Frontend、Backend、Database を分離し、バックエンドは
Controller・Repository・Domain を中心としたレイヤード構成を採用しています。
Service 相当のユースケース処理は、現状は専用レイヤーとして分離せず、routers / utils / batch に分散して実装しています。

- Controller: API の入出力、認証依存、HTTP ステータスの制御を担当
- Service（現状）: 専用層は設けず、ユースケース単位の処理を routers / utils / batch で実装
- Repository: DB アクセスを担当し、永続化の詳細を隠蔽
- Domain: エンティティ、Enum、業務ルール（ステータスや制約）を保持
- Frontend: ルートは feature-based、各 feature 内は type-based で整理し、features / shared で責務を分離
- Frontend（参考）: https://zenn.dev/bln/articles/986b709f4df0c1

### バックエンド設計のポイント

- `controllers(routers)` でエンドポイントごとの責務を分離
- `service` は専用ディレクトリを設けず、`routers` / `utils` / `batch` に分散してユースケースを実装
- `schemas` でリクエスト/レスポンスの型とバリデーションを管理
- `repository` で DB 操作を集約
- `domain(models, enums)` で業務ルールと状態を表現
- `exception_handler` で例外レスポンスを統一

### フロントエンド設計のポイント

- `features/tasks` と `features/users` に機能を分離
- `shared/components` に再利用 UI を集約
- `react-hook-form` を使ってフォームバリデーションを統一
- 認証やAPI 呼び出しをHook / Provider に分離して見通しを保つ

## 工夫した点

### 1. AI タスク生成をアプリの中心機能にしたこと
単にAIへ自由入力を渡すのではなく、目標、現状、期限、可用時間、追加条件を構造化して渡すことで、実行可能性の高いタスク案を生成できるようにしています。

### 2. JWT認証におけるセキュリティとユーザビリティの両立
アクセストークンは短い有効期限に設定し、期限切れ時はリフレッシュトークンで再発行する構成にすることで、セキュリティと継続利用の両立を図りました。

また、リフレッシュトークンはDBで管理し、ログアウト時や不正利用検知時に失効できる設計としています。トークンは平文保存せずハッシュ化して保存し、照合時はトークンプレフィックスで候補を絞り込んでからハッシュ照合することで、安全性と検索効率の両立を意識しました。

### 3. 多層バリデーションによるユーザビリティとデータ整合性の両立
入力値の検証はフロントエンド・API・データベースで役割を分けて実装しています。

フロントエンドでは必須入力や形式チェックなど、ユーザーへ即座にフィードバックを返す軽量なバリデーションを行っています。日付入力では形式だけでなく、Day.jsを用いて実在する日付かどうかも検証しています。

メールアドレスはフロント側でも簡易的な形式チェックを行いつつ、バックエンドではPydantic（EmailStr）で厳密に検証する構成とし、不正なリクエストを防止しています。

さらに、DB側でもCheck ConstraintやForeign Key制約を定義し、アプリケーション不具合や想定外の入力が発生した場合でも不正データが保存されないようにしています。

### 4. 一貫した例外レスポンス設計
HTTP例外、業務例外、バリデーション例外を共通フォーマットで返すように統一しました。これにより、フロントエンド側で例外ハンドリングを実装しやすくし、API利用時の予測可能性を高めています。

## ディレクトリ構成

```text
todo-app/
├─ .github/
│  └─ workflows/
│     ├─ ci.yml
│     └─ depoloy.yml
├─ backend/
│  ├─ alembic/
│  │  └─ versions/
│  ├─ batch/
│  ├─ container/
│  │  ├─ fastapi/
│  │  └─ postgres/
│  ├─ exceptions/
│  ├─ models/
│  ├─ repository/
│  ├─ routers/
│  ├─ schemas/
│  ├─ utils/
│  └─ test/
│     ├─ integration/
│     └─ unit/
├─ frontend/
│  ├─ public/
│  └─ src/
│     ├─ assets/
│     ├─ features/
│     │  ├─ tasks/
│     │  └─ users/
│     └─ shared/
│        ├─ api/
│        ├─ components/
│        ├─ hooks/
│        └─ types/
├─ .env.example
├─ docker-compose.yml
└─ README.md
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

最短の起動手順:

1. ルートディレクトリに `.env` を作成（`.env.example` を参照）
2. 以下を実行

```bash
docker compose up -d --build
```

本番環境の参照先:

- Frontend: https://claidy-todo.com
- Backend API Docs: https://claidy-todo.com/api/docs

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
