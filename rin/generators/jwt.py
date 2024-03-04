import jwt
from starlette.authentication import (AuthenticationBackend, 
                                      AuthenticationError)
from pydantic import BaseModel

class UserJWT(BaseModel):
    name: str
    email: str
    access_level: int

async def generate_jwt(user: UserJWT) -> str:
    return jwt.encode({
        'name': user.name,
        'email': user.email,
        'access_level': user.access_level
    },
    "segredo",
    algorithm='HS256')

# Authentication Backend Class
class BearerTokenAuthBackend(AuthenticationBackend):
    """
    This is a custom auth backend class that will allow you to authenticate your request and return auth and user as
    a tuple
    """
    async def authenticate(self, request):
        # This function is inherited from the base class and called by some other class
        if "Authorization" not in request.headers:
            return

        auth = request.headers["Authorization"]
        try:
            scheme, token = auth.split()
            if scheme.lower() != 'bearer':
                return
            decoded = jwt.decode(token, "segredo", algorithms=['HS256'])
        except (ValueError, UnicodeDecodeError, jwt.PyJWTError) as exc:
            raise AuthenticationError('Invalid JWT Token.')

        user = UserJWT(name=decoded.get('name'),
                       email=decoded.get('email'),
                       access_level=decoded.get('access_level'))

        if user is None:
            raise AuthenticationError('Invalid JWT Token.')
        
        return auth, user