from typing import Literal

from pydantic import BaseModel


class Model(BaseModel):
    id: str
    object: Literal["model"] = "model"
    created: int
    owned_by: str
