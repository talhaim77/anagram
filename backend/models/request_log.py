from sqlalchemy import Column, String, Integer, DateTime, Float

from backend.database.connection import Base
from datetime import datetime, timezone

class RequestLog(Base):
    __tablename__ = 'request_log'

    id = Column(Integer, primary_key=True)
    endpoint = Column(String, index=True)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc), index=True)
    processing_time = Column(Float)
    word = Column(String, nullable=True)
