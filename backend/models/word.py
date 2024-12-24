from os import getenv
from sqlalchemy import Column, String, Integer
from backend.database.connection import Base


WORD_MAX_LENGTH = int(getenv("WORD_MAX_LENGTH", 100))


class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String(WORD_MAX_LENGTH), unique=True, nullable=False)
    sorted_word = Column(String, index=True, nullable=False)