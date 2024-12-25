from datetime import datetime, timezone

from time import time
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy import select, DateTime, Column
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models.request_log import RequestLog
from models.word import Word
from dependencies import get_db_session
from schemas.word_schemas import SimilarWordsResponse, AddWordResponse, AddWordRequest
from settings import settings as app_config
from utils.string_utils import compute_letter_frequency

router = APIRouter()


@router.get("/similar",
            response_model=SimilarWordsResponse,
            status_code=status.HTTP_200_OK,
            summary="Retrieve similar words")
async def get_similar_words(
        word: str = Query(..., min_length=1),
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
        db=db,
        word=word
    )

    return SimilarWordsResponse(similar=list(similar))


@router.post(
    "/add-word", response_model=AddWordResponse,
    status_code=status.HTTP_200_OK,
    summary="Add a new word to the database")
async def add_word(
    add_word_request: AddWordRequest,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Adds a new word to the dictionary for future queries.

    Args:
        add_word_request (AddWordRequest): The word to add.
        db (AsyncSession): db session.

    Returns:
        AddWordResponse: Success message.
    """

    word_to_store = add_word_request.word.strip().lower()
    word_signature = compute_letter_frequency(word_to_store)

    new_word = Word(word=word_to_store, signature=word_signature)
    try:
        start_time = time()
        db.add(new_word)
        await db.commit()
        await db.refresh(new_word)
        end_time = time()
    except IntegrityError:
        end_time = time()
        await db.rollback()

        processing_time = (end_time - start_time) * 1_000_000
        await log_request(
            endpoint=f"/api/{app_config.API_VERSION}/add-word",
            processing_time=processing_time,
            db=db,
            word=word_to_store
        )

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

    return AddWordResponse(message=f"Word: {add_word_request.word} added successfully")


async def fetch_similar_words(word: str, db: AsyncSession):
    """
    Todo: add docstring
    """
    word_signature = compute_letter_frequency(word.lower().strip())

    statement = (
        select(Word.word)
        .where(Word.signature == word_signature)
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


async def log_request(endpoint, processing_time, db, word: Optional[str] = None):
    log = RequestLog(
        endpoint=endpoint,
        processing_time=processing_time,
        word=word,
    )
    try:
        db.add(log)
        await db.commit()
        await db.refresh(log)
        print(f"log_request: {endpoint} successfully")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to log the request: {e}")
