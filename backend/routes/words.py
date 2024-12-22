from typing import List
from fastapi import APIRouter, HTTPException

from backend.database.connection import get_connection

router = APIRouter()

@router.get("/similar/{word}", response_model=List[str])
async def get_similar_words(word: str) -> List[str]:
    """
    Retrieve all words in the dataset that share the same sorted character tuple as the given word.

    Args:
        word (str): The word to find similar words for.

    Returns:
        List[str]: A list of words that share the same sorted character tuple as the input word,
         excluding the word itself.

    Raises:
        HTTPException: If no similar words are found.
    """
    sorted_word = tuple(sorted(word))

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT word FROM words WHERE sorted_word = %s", (''.join(sorted_word),))
            results = [row[0] for row in cur.fetchall() if row[0] != word]

    if results:
        return results
    else:
        raise HTTPException(status_code=404, detail="Similar words not found")