from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.word import Word
from backend.dependencies import get_db_session
from backend.schemas.word_schemas import SimilarWordsResponse

router = APIRouter()


@router.get("/similar", response_model=SimilarWordsResponse)
async def get_similar_words(
        word: str = Query(...),
        db: AsyncSession = Depends(get_db_session)
):
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
        similar = result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {e}")

    if not similar:
        raise HTTPException(status_code=404, detail="Similar words not found")

    return SimilarWordsResponse(similar=list(similar))