from fastapi import FastAPI, APIRouter
from backend.settings import settings as app_config
from backend.lib.lifespan import lifespan
from backend.api.word_router import router as words_router
from backend.api.request_log_route import router as stats_router


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
app.include_router(stats_router, prefix=f'/api/{app_config.API_VERSION}')