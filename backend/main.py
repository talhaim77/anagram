from fastapi import FastAPI, APIRouter
from backend.settings import settings as app_config
from backend.lib.lifespan import lifespan
from backend.api.word_route import router as words_router



app = FastAPI(
    title=app_config.TITLE,
    description=app_config.DESCRIPTION,
    version=app_config.API_VERSION,
    lifespan=lifespan
)

api_router = APIRouter()
api_router.include_router(words_router, tags=["Word"])

app.include_router(api_router,
                   prefix=f'/api/{app_config.API_VERSION}'
                   )