from typing import Literal

from pydantic import BaseModel


class Check(BaseModel):
    name: str
    status: Literal["ok", "error"]
    error: str | None
