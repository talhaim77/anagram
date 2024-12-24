from sqlalchemy import Column, String, Integer

from backend.database.connection import Base


class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String, unique=True, nullable=False)
    sorted_word = Column(String, index=True, nullable=False)