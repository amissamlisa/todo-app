from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from unittest import TestCase
from starlette.testclient import TestClient

from backend.database import get_db
from backend.main import app
from backend.models.models import Base
from urllib.parse import quote_plus
# .envファイルから環境変数を読み込む
load_dotenv()
# 環境変数取得
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")

# パスワードやユーザー名を URL エンコード
password_enc = quote_plus(password)
user_enc = quote_plus(user)

# SQLAlchemy 用 URL 作成
SQLALCHEMY_TEST_DATABASE_URL = (
    f"postgresql+psycopg2://{user_enc}:{password_enc}@{host}:{port}/{dbname}"
    f"?client_encoding=utf8"
)
print(SQLALCHEMY_TEST_DATABASE_URL)
if not all([user, password, host, port, dbname]):
    raise ValueError("DB接続に必要な環境変数が設定されていません")

# SQLAlchemyのエンジンを作成
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    pool_size=10,  # Number of connections to keep in the pool
    max_overflow=20,  # Number of connections to allow in overflow
    pool_timeout=30,  # Seconds to wait before giving up on getting a connection
    pool_recycle=1800,  # Recycle connections after 30 minutes
    pool_pre_ping=True,  # Check connections before using
    echo=os.getenv("SQLALCHEMY_ECHO", "False").lower() == "true"  # Debug logging
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_testing():
    db = TestingSessionLocal(bind=engine)
    try:
        yield db
        db.rollback()
    finally:
        db.close()

app.dependency_overrides[get_db] = get_db_testing

client = TestClient(app)