from fastapi import APIRouter

from .models import router as modelsRouter

router = APIRouter(prefix="/v1")

router.include_router(modelsRouter)
