
from typing import List
from pydantic import BaseModel

class SimilarWordsResponse(BaseModel):
    similar: List[str]

    class Config:
        from_attributes = True
