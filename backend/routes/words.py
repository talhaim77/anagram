from typing import List
from fastapi import APIRouter, Request, HTTPException


router = APIRouter()

@router.get("/similar/{word}", response_model=List[str])
async def get_similar_words(word: str, request: Request) -> List[str]:
    """
    Given a word, return all words in the dataset that share the same
    sorted character tuple.
    """
    word_dict = request.app.state.word_dict

    sorted_word = tuple(sorted(word))
    if sorted_word in word_dict:
        return word_dict[sorted_word]
    else:
        raise HTTPException(status_code=404, detail="Similar words not found")