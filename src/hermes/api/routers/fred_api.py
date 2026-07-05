from fastapi import APIRouter
from pydantic import Field, BaseModel

router = APIRouter()

@router.get()
def get():
    pass