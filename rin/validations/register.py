from fastapi import UploadFile
from pydantic import BaseModel

class NewUser(BaseModel):
    name: str
    email: str