import jwt
from pydantic import BaseModel

class UserJWT(BaseModel):
    name: str
    email: str
    access_level: int

def generate_jwt(user: UserJWT) -> str:
    return jwt.encode({
        'name': user.name,
        'email': user.email,
        'access_level': user.access_level
    },
    "segredo",
    algorithm='HS256')