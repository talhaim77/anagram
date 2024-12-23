from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

"""
CREATE TABLE IF NOT EXISTS words (
                     word TEXT PRIMARY KEY,
                     sorted_word TEXT
);
"""

class Word(Base):
    __tablename__ = 'words'

    word = Column(String, primary_key=True, nullable=False)
    sorted_word = Column(String, nullable=False)
