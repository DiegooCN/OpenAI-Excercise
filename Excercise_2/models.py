from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    dni: str
    name: str
    message: str

class Context(BaseModel):
    user: User
    content: Optional[str] = None
    role: Optional[str] = None
    function: Optional[str] = None