from fastapi import FastAPI

from src.hermes.api.routers.fred_api import router as fred_router
from src.hermes.database.database import check_db_health_async, init_db_async

app = FastAPI(
    version='0.1.0',
    description='A data platform for Aiges and other projects'
)


@app.on_event("startup")
async def startup_event() -> None:
    await init_db_async()


@app.get('/')
def root():
    return {'service': 'hermes'}


@app.get('/health')
async def health():
    return {'status': 'ok'}

@app.get('/db_health')
async def db_health():
    return await check_db_health_async()

app.include_router(fred_router)
