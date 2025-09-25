from pydantic import BaseModel
from datetime import datetime

class Msg(BaseModel):
    detail: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: str
    role: str
    exp: int | None = None