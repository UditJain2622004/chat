from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    uid: str
    email: EmailStr
    name: Optional[str] = None
    picture: Optional[str] = None
