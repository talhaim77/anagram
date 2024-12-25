from sqlalchemy import String, Integer, DateTime, Float
from sqlalchemy.orm import mapped_column, Mapped

from backend.database.connection import Base
from datetime import datetime, timezone

class RequestLog(Base):
    __tablename__ = 'request_log'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    endpoint: Mapped[str] = mapped_column(String, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc), index=True)
    processing_time: Mapped[float] = mapped_column(Float)
    word: Mapped[str] = mapped_column(String, nullable=True)

    def __repr__(self) -> str:
        return f"RequestLog(id={self.id}, endpoint='{self.endpoint}')"