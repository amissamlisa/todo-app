from datetime import datetime, timezone
import logging
from backend.database import SessionLocal
from backend.repository.repository import (
    RefreshTokenRepository,
    PasswordResetRepository,
)


def cleanup_expired_tokens() -> dict[str, int]:
    now = datetime.now(timezone.utc)
    refresh_repo = RefreshTokenRepository()
    password_repo = PasswordResetRepository()

    db = SessionLocal()
    try:
        refresh_deleted = refresh_repo.delete_expired_refresh_tokens(
            db, now=now, commit=False
        )
        password_deleted = password_repo.delete_expired_password_reset_tokens(
            db, now=now, commit=False
        )
        db.commit()
        return {
            "refresh_tokens_deleted": refresh_deleted,
            "password_reset_tokens_deleted": password_deleted,
        }
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    result = cleanup_expired_tokens()
    logger.info(
        "Cleanup complete. refresh=%s password=%s",
        result["refresh_tokens_deleted"],
        result["password_reset_tokens_deleted"],
    )

if __name__ == "__main__":
    main()