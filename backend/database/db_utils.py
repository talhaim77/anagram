from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncEngine
from fastapi import Depends
from backend.database.models import Word
from backend.dependencies import get_db_session
from backend.database.models import Base


async def initialize_tables(engine: AsyncEngine) -> None:
    """
    Creating all tables defined in the SQLAlchemy Base metadata
    into the database.

    Args:
        engine (AsyncEngine): SQLAlchemy engine instance

    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def load_word_dataset(dataset_path: Path, db_session = Depends(get_db_session)):
    """
    Load a dataset of words into the Word table.

    This function reads a file containing a list of words, sort each word alphabetically,
    and stores the original word along with its sorted version in the db.

    Args:
        dataset_path (Path): Path to the dataset.
        db_session: db session dependency

    Raises:
        Exception: If an error occurs while loading the dataset.
    """
    try:
        with open(dataset_path, 'r') as f:
            words = [line.strip() for line in f.readlines()]

        for word in words:
            sorted_word = ''.join(sorted(word))
            db_session.add(Word(word=word, sorted_word=sorted_word))

        await db_session.commit()
        print("Dataset loaded into Word table.")
    except Exception as e:
        print(f"Error loading dataset: {e}")
        await db_session.rollback()