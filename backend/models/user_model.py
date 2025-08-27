from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserDetails(BaseModel):
    name: Optional[str] = None

    nickname: Optional[str] = None
    available_timings: Optional[str] = None
    task_following_record: list[str] = Field(default_factory=list)
    preferences: list[str] = Field(default_factory=list)
    dislikes: list[str] = Field(default_factory=list)
    anything_else: list[str] = Field(default_factory=list)
    
    updated_at: datetime = Field(default_factory=datetime.now)

class User(BaseModel):
    uid: str
    email: EmailStr
    picture: Optional[str] = None

    user_details: UserDetails = Field(default_factory=UserDetails)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    

    bot_ids: List[str] = Field(default_factory=list)
