from os import getenv
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from database.connection import Base


WORD_MAX_LENGTH = int(getenv("WORD_MAX_LENGTH", 100))


class Word(Base):
    __tablename__ = 'words'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    word: Mapped[str] = mapped_column(String(WORD_MAX_LENGTH), unique=True, nullable=False)
    signature: Mapped[str] = mapped_column(String(26), index=True, nullable=False)

    def __repr__(self) -> str:
        return f"Word(id={self.id}, word='{self.word}')"