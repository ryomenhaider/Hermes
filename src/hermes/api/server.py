from fastapi import FastAPI

app = FastAPI(
    version='0.1.0',
    description='A data platform for Aiges and other projects'
)


@app.get('/')
def root():
    return {'service': 'hermes'}

@app.get('/health')
def health():
    return {'status': 'ok'}

