from datetime import datetime

from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from models import BlacklistedToken


class BlacklistedTokenRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def is_blacklisted(self, token: str) -> bool:
        return (
            self.db.query(BlacklistedToken)
            .filter(BlacklistedToken.token == token)
            .first()
            is not None
        )

    def add(self, token: str, expires_at: datetime) -> None:
        self.db.add(BlacklistedToken(token=token, expires_at=expires_at))
        self.db.commit()


def get_blacklisted_token_repository(
    db: Session = Depends(get_db),
) -> BlacklistedTokenRepository:
    return BlacklistedTokenRepository(db)
