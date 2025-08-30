from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

#.envファイルから環境変数を読み込む
load_dotenv()

#データベースURLを取得
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

if SQLALCHEMY_DATABASE_URL is None:
    raise RuntimeError("Environment variable 'SQLALCHEMY_DATABASE_URL' is not set.")

#SQLAlchemyのエンジンを作成
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#セッションクラスを作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()