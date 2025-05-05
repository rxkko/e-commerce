from pydantic import BaseModel

class Token(BaseModel):
    token: str

class TokenData(BaseModel):
    id: int
    email: str
    is_admin: bool