
from typing import List
from pydantic import BaseModel, Field
from os import getenv

WORD_MAX_LENGTH = int(getenv("WORD_MAX_LENGTH", 100))

class SimilarWordsResponse(BaseModel):
    similar: List[str]

    class Config:
        from_attributes = True


class AddWordRequest(BaseModel):
    word: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="The word to add to the dictionary."
    )


class AddWordResponse(BaseModel):
    message: str = Field(...,
                         description="Success message.")