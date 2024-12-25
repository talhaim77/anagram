from pathlib import Path

import aiofiles
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import select, func
from fastapi import Depends
from models.word import Word
from dependencies import get_db_session
from models.word import Base
import logging

from utils.string_utils import compute_letter_frequency

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CHUNK_SIZE = 1000


async def initialize_tables(engine: AsyncEngine) -> None:
    """
    Creating all tables defined in the SQLAlchemy Base metadata
    into the database.

    Args:
        engine (AsyncEngine): SQLAlchemy engine instance

    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Connection test successful")


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
        async with aiofiles.open(dataset_path, 'r') as f:
            words = [line.strip().lower() async for line in f if line.strip()]  # type: ignore

        total_words = len(words)

        # similar to sql: SELECT COUNT(*) FROM Word;
        stmt = select(func.count()).select_from(Word)
        result = await db_session.execute(stmt)
        word_count = result.scalar_one()

        if word_count >= total_words:
            logger.info("Word table already populated. Skipping dataset load.")
            return

        logger.info(f"Loading words dataset from: {dataset_path}")

        # Fetch existing words from the database
        existing_words = set()
        for i in range(0, len(words), CHUNK_SIZE):
            chunk = words[i:i + CHUNK_SIZE]
            stmt = select(Word.word).where(Word.word.in_(chunk))
            result = await db_session.execute(stmt)
            existing_words.update(result.scalars().all())

        new_words = [
            Word(word=word,
                 signature=compute_letter_frequency(word)
            )
            for word in words
            if word not in existing_words
        ]

        if new_words:
            db_session.add_all(new_words)
            await db_session.commit()
            logger.info(f"{len(new_words)} new words added to the Word table.")
        else:
            logger.info("No new words to add. All words already exist.")

    except Exception as e:
        await db_session.rollback()
        print(f"Error loading word dataset: {e}")
        raise