from typing import List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models import Word
from backend.dependencies import get_db_session

router = APIRouter()


@router.get("/similar/{word}", response_model=List[str])
async def get_similar_words(word: str, db: AsyncSession = Depends(get_db_session)):
    """
    Retrieve all words in the dataset that share the same sorted character tuple as the given word.

    Args:
        word (str): The word to find similar words for.
        db (AsyncSession): Database session.
    Returns:
        List[str]: A list of words that share the same sorted character tuple as the input word,
         excluding the word itself.

    Raises:
        HTTPException: If no similar words are found.
    """
    sorted_word = str(''.join(sorted(word)))

    statement = (
        select(Word.word)
        .where(Word.sorted_word == sorted_word)
        .where(Word.word != word)
    )
    try:
        result = await db.execute(statement)
        words = result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {e}")

    if not words:
        raise HTTPException(status_code=404, detail="Similar words not found")

    return SimilarWordsResponse(words=list(words))