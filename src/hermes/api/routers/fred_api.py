from fastapi import APIRouter, HTTPException

from hermes.connectors.fred.client import FredClient

router = APIRouter(prefix='/fred', tags=['fred'])


@router.get('/metadata')
def get_metadata():
    client = FredClient()
    try:
        return client.get_data('metadata')
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get('/observations')
def get_observations():
    client = FredClient()
    try:
        return client.get_data('observations')
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
