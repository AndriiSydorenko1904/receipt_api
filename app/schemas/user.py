from __future__ import annotations
from pydantic import BaseModel


class UserRegister(BaseModel):
    name: str
    login: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = {
        "from_attributes": True
    }
