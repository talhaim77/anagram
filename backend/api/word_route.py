from datetime import datetime, timezone

from time import time
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy import select, DateTime, Column
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.models.request_log import RequestLog
from backend.models.word import Word
from backend.dependencies import get_db_session
from backend.schemas.word_schemas import SimilarWordsResponse, AddWordResponse, AddWordRequest
from backend.settings import settings as app_config

router = APIRouter()


@router.get("/similar",
            response_model=SimilarWordsResponse,
            status_code=status.HTTP_200_OK,
            summary="Retrieve similar words")
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
        HTTPException: No similar words found.
    """

    similar, processing_time = await fetch_similar_words(word, db)

    if not similar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Similar words not found")

    await log_request(
        endpoint=f"/api/{app_config.API_VERSION}/similar",
        processing_time=processing_time,
        db=db
    )

    return SimilarWordsResponse(similar=list(similar))


async def log_request(endpoint, processing_time, db):
    log = RequestLog(
        endpoint=endpoint,
        processing_time=processing_time,
    )
    try:
        db.add(log)
        await db.commit()
        await db.refresh(log)
        print(f"log_request: {endpoint} successfully")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to log the request: {e}")


async def fetch_similar_words(word: str, db: AsyncSession):

    sorted_word = ''.join(sorted(word))
    statement = (
        select(Word.word)
        .where(Word.sorted_word == sorted_word)
        .where(Word.word != word)
    )
    try:
        start_time = time()
        result = await db.execute(statement)
        similar = result.scalars().all()
        end_time = time()
        processing_time = (end_time - start_time) * 1_000_000
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database query failed: {e}"
        )
    return similar, processing_time


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
        start_time = time()
        db.add(new_word)
        await db.commit()
        await db.refresh(new_word)
        end_time = time()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Word already exists in database"
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to add word: {e}")

    processing_time = (end_time - start_time) * 1_000_000

    await log_request(
        endpoint=f"/api/{app_config.API_VERSION}/add-word",
        processing_time=processing_time,
        db=db
    )

    return AddWordResponse(message=f"Word: {add_word.word} added successfully")

