from fastapi import APIRouter, HTTPException
from .response import Response

router = APIRouter(prefix="/models", tags=["OpenAI - models"])


@router.get("/")
def get_models() -> Response:
    raise HTTPException(status_code=501, detail="Not implemented")
