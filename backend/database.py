from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
# .envファイルから環境変数を読み込む
load_dotenv()


# テスト用データベース
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
if SQLALCHEMY_DATABASE_URL is None:
    raise RuntimeError( "Environment variable 'SQLALCHEMY_DATABASE_URL' is not set.\n"
        "Please set this variable in your environment or create a .env file in the project root with a line like:\n"
        "SQLALCHEMY_DATABASE_URL=SQLALCHEMY_DATABASE_URL"
    )

# SQLAlchemyのエンジンを作成
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=10,            # Number of connections to keep in the pool
    max_overflow=20,         # Number of connections to allow in overflow
    pool_timeout=30,         # Seconds to wait before giving up on getting a connection
    pool_recycle=1800,       # Recycle connections after 30 minutes
    pool_pre_ping=True,      # Check connections before using
    echo=os.getenv("SQLALCHEMY_ECHO", "False").lower() == "true"  # Debug logging
    )

# セッションクラスを作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()