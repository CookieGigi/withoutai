from .default import router as defaultRouter
from .health import router as healthRouter
from .models import router as modelsRouter

__all__ = ["defaultRouter", "healthRouter", "modelsRouter"]
