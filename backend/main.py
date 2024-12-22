from fastapi import FastAPI
import aiofiles
from contextlib import asynccontextmanager
from routes.words import router as words_router

app = FastAPI()


async def load_words(file_path: str):
    """
    Asynchronously load words from a file
    and group them by their sorted character tuple.
    """
    word_dict = {}
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


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(words_router)

    return app

app = create_app()