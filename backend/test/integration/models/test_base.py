from unittest import TestCase

from backend.test.test_setup import engine, client, get_db_testing
from backend.models.models import Base

class TestBase(TestCase):
    def setUp(self):
        # テーブル作成
        Base.metadata.create_all(bind=engine)
        # DBセッション作成
        db_gen = get_db_testing()
        self.db = next(db_gen)
        # テストクライアント作成
        self.client = client

    def tearDown(self):
        self.db.rollback()
        self.db.close()
        Base.metadata.drop_all(bind=engine)