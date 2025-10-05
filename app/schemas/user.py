from pydantic import BaseModel

# Model for registering/loggin in a user
class UserCreate(BaseModel):
    username: str
    password: str

# Model for returning user info in responses
class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

# Model for JWT token's response
class Token(BaseModel):
    access_token: str
    token_type: str
