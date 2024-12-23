from fastapi import FastAPI, APIRouter
from backend.config import settings as app_config
from backend.lib.lifespan import lifespan
from backend.routes.words import router as words_router



app = FastAPI(**app_config, lifespan=lifespan)

api_router = APIRouter()
api_router.include_router(words_router, tags=["Word"])

app.include_router(api_router,
                   prefix=f'/api/{app_config.API_VERSION}'
                   )