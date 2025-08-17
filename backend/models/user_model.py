from pydantic import BaseModel, EmailStr
from typing import Optional, List

class User(BaseModel):
    uid: str
    email: EmailStr
    name: Optional[str] = None
    picture: Optional[str] = None
    

    bot_ids: List[str] = []
