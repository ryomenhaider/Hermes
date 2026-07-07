from fastapi import APIRouter, HTTPException

from src.hermes.connectors.fred.client import FredClient
from src.hermes.database.database import query_all_async
from src.hermes.models.fred_model import FredObs

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

@router.get('/{indicator}/{limit}')
async def get_indicator(indicator: str, limit: int = 10):
    value = await query_all_async(model=FredObs, limit=limit, series_id=indicator)
    return value