from pydantic import BaseModel

class User(BaseModel):
    id: str
    name: str
    message: str

class Context(BaseModel):
    user: User
    content: str
    role: str
    function: str