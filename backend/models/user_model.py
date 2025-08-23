from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class BotAndChat(BaseModel):
    bot_id: str
    chat_ids: List[str] = Field(default_factory=list)

class User(BaseModel):
    uid: str
    email: EmailStr
    name: Optional[str] = None
    picture: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    

    bot_ids: List[str] = Field(default_factory=list)
