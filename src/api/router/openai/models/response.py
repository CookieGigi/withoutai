from typing import Literal

from pydantic import BaseModel


class Response(BaseModel):
    id: str
    object: Literal["model"]
    created: int
    owned_by: str
