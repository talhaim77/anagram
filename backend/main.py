from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
import os

from backend.config import settings as app_config
from backend.database.db_utils import load_words_to_db
from backend.database.connection import init_db
from backend.routes.words import router as words_router


@asynccontextmanager
def lifespan(app: FastAPI):
    """
    Manage the application lifespan, including setting up the db.
    The dataset file path can be configured via the WORDS_DATASET_PATH environment variable.
    """
    dataset_path = os.getenv("WORDS_DATASET_PATH", "backend/dataset/words_dataset.txt")
    init_db()
    load_words_to_db(dataset_path)
    yield


app = FastAPI(lifespan=lifespan)

api_router = APIRouter()
api_router.include_router(words_router, tags=["Word"])

app.include_router(api_router,
                   prefix=f'/api/{app_config.API_VERSION}'
                   )