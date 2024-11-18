from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str


class User(BaseModel):
    id: int
    username: str
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str
