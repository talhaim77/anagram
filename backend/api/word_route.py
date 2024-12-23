from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.models.word import Word
from backend.dependencies import get_db_session
from backend.schemas.word_schemas import SimilarWordsResponse, AddWordResponse, AddWordRequest

router = APIRouter()


@router.get("/similar",
            response_model=SimilarWordsResponse,
            status_code=status.HTTP_200_OK,
            summary=...)
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
    sorted_word = ''.join(sorted(word))

    statement = (
        select(Word.word)
        .where(Word.sorted_word == sorted_word)
        .where(Word.word != word)
    )
    try:
        result = await db.execute(statement)
        similar = result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Database query failed: {e}")

    if not similar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Similar words not found")

    return SimilarWordsResponse(similar=list(similar))

@router.post(
    "/add-word", response_model=AddWordResponse,
    status_code=status.HTTP_200_OK,
    summary="Add a new word to the database")
async def add_word(
    add_word: AddWordRequest,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Adds a new word to the dictionary for future queries.

    Args:
        add_word (AddWordRequest): The word to add.
        db (AsyncSession): db session.

    Returns:
        AddWordResponse: Success message.
    """

    word_to_store = add_word.word.strip().lower()
    sorted_word = str(''.join(sorted(word_to_store)))
    new_word = Word(word=word_to_store, sorted_word=sorted_word)
    try:
        db.add(new_word)
        await db.commit()
        await db.refresh(new_word)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Word already exists in database"
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to add word: {e}")

    return AddWordResponse(message=f"Word: {add_word.word} added successfully")

