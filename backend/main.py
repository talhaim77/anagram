from fastapi import FastAPI, APIRouter

from middlewares import register_middlewares
from settings import settings as app_config
from lib.lifespan import lifespan
from api.word_router import router as words_router
from api.request_log_router import router as stats_router


app = FastAPI(
    title=app_config.TITLE,
    description=app_config.DESCRIPTION,
    version=app_config.API_VERSION,
    lifespan=lifespan
)

register_middlewares(app)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

api_router = APIRouter()
api_router.include_router(words_router, tags=["Word"])

app.include_router(api_router,
                   prefix=f'/api/{app_config.API_VERSION}'
                   )
app.include_router(stats_router, prefix=f'/api/{app_config.API_VERSION}')

