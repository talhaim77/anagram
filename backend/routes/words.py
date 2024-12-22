from typing import List
from fastapi import APIRouter, Request, HTTPException


router = APIRouter()

@router.get("/similar/{word}", response_model=List[str])
async def get_similar_words(word: str, request: Request) -> List[str]:
    """
    Retrieve all words in the dataset that share the same sorted character tuple as the given word.

    Args:
        word (str): The word to find similar words for.
        request (Request): The FastAPI request object.

    Returns:
        List[str]: A list of words that share the same sorted character tuple as the input word,
         excluding the word itself.

    Raises:
        HTTPException: If no similar words are found.
    """
    word_dict = request.app.state.word_dict
    sorted_word = tuple(sorted(word))

    if sorted_word in word_dict:
        similar_words = [w for w in word_dict[sorted_word] if w != word]
    else:
        raise HTTPException(status_code=404, detail="Similar words not found")

    return similar_words