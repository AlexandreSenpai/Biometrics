from contextlib import asynccontextmanager
import typing
from fastapi import FastAPI, File, Form, Response, UploadFile, status, HTTPException
from prisma import Prisma
import imagehash
from rin.generators.jwt import UserJWT, generate_jwt

from rin.processors.image import process_image

@asynccontextmanager
async def lifespan(server: FastAPI):
    await db.connect()
    yield
    await db.disconnect()

server = FastAPI(lifespan=lifespan)

db = Prisma()

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

    if restored_hash - new_hash <= 20:
        
        user = UserJWT(name=stored_user.name,
                       email=stored_user.email,
                       access_level=stored_user.access_level)
        
        response.set_cookie('RIN_TOKEN', generate_jwt(user))
        return { 'authenticated': True }
    
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return { 'authenticated': False }

