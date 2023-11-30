from pydantic import BaseModel

class User(BaseModel):
    id: str = "1"
    name: str = "Diego"
    message: str = "Hola"

class Context(BaseModel):
    user: User
    content: str
    role: str
    function: str