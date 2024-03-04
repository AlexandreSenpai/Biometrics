from contextlib import asynccontextmanager
import typing
from fastapi import FastAPI, File, Form, Request, Response, UploadFile, status, HTTPException
from starlette.middleware.authentication import AuthenticationMiddleware 
from prisma import Prisma
import imagehash
from rin.generators.jwt import BearerTokenAuthBackend, UserJWT, generate_jwt

from rin.processors.image import process_image

db = Prisma()

@asynccontextmanager
async def lifespan(server: FastAPI):
    await db.connect()
    yield
    await db.disconnect()

server = FastAPI(lifespan=lifespan) # type: ignore

server.add_middleware(AuthenticationMiddleware, backend=BearerTokenAuthBackend())

@server.post('/register')
async def register(name: typing.Annotated[str, Form()],
                   email: typing.Annotated[str, Form()],
                   biometric: typing.Annotated[UploadFile, File()],
                   response: Response):
    
    img = await biometric.read()
    img = process_image(img)
    bio_hash = imagehash.average_hash(img)

    user = await db.user.create({
        'name': name,
        'email': email,
        'bio_hash': str(bio_hash) 
    })

    response.status_code = status.HTTP_201_CREATED
    return user.model_dump()

@server.post('/login')
async def login(email: typing.Annotated[str, Form()], 
                biometric: typing.Annotated[UploadFile, File()],
                response: Response):

    stored_user = await db.user.find_unique({
        'email': email 
    })

    if stored_user is None: 
        raise HTTPException(status_code=400, detail='Provided user does not exists.')
    
    new_bio_bytes = await biometric.read()
    new_bio_bytes = process_image(new_bio_bytes)
    new_hash = imagehash.average_hash(new_bio_bytes)
    stored_hash = stored_user.bio_hash
    restored_hash = imagehash.hex_to_hash(stored_hash)

    print(restored_hash - new_hash)
    print(restored_hash == new_hash)

    if restored_hash - new_hash <= 20:
        
        user = UserJWT(name=stored_user.name,
                       email=stored_user.email,
                       access_level=stored_user.access_level)
        
        response.set_cookie('RIN_TOKEN', await generate_jwt(user))
        return { 'authenticated': True }
    
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return { 'authenticated': False }

@server.get('/stock')
async def stock(request: Request):
    stock = await db.stock.find_many()

    return list(filter(lambda x: x.access_level <= request.user.access_level, stock))

@server.get('/agrotoxic')
async def agrotoxic(request: Request):
    agrotoxic = await db.agrotoxic.find_many(include={ 'stock': True })
    
    return list(filter(lambda x: x.access_level <= request.user.access_level, agrotoxic))

@server.get('/ruralProperties')
async def rural_properties(request: Request):
    properties = await db.ruralproperty.find_many(include={ 
        'agrotoxics': { 
            'include': { 
                'agrotoxic': {
                    'include': {
                        'stock': True
                    }
                }
            }
        }
    })

    return list(filter(lambda x: x.access_level <= request.user.access_level, properties))