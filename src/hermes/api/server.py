from fastapi import FastAPI

from hermes.api.routers.fred_api import router as fred_router

app = FastAPI(
    version='0.1.0',
    description='A data platform for Aiges and other projects'
)

app.include_router(fred_router)


@app.get('/')
def root():
    return {'service': 'hermes'}


@app.get('/health')
def health():
    return {'status': 'ok'}

