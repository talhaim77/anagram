from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from typing import Dict, List, Tuple
import aiofiles

from config import settings as app_config
from routes.words import router as words_router


async def load_words(file_path: str):
    """
    Asynchronously load words from a file
    and group them by their sorted character tuple.
    """
    word_dict: Dict[Tuple[str, ...], List[str]] = {}
    async with aiofiles.open(file_path, mode='r') as file:
        async for line in file:
            word = line.strip()
            sorted_word = tuple(sorted(word))
            word_dict.setdefault(sorted_word, []).append(word)
        return word_dict


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.word_dict = await load_words('dataset/words_dataset.txt')
    yield


app = FastAPI(lifespan=lifespan)

api_router = APIRouter()
api_router.include_router(words_router, tags=["Word"])

app.include_router(api_router,
                   prefix=f'/api/{app_config.API_VERSION}'
                   )