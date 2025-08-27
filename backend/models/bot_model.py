from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime

class BotDetails(BaseModel):
    name: str
    picture: Optional[str] = None
    description: Optional[str] = None

    likings: list[str] = []  # pro at these things
    behaviour: Literal['friendly', 'neutral', 'sassy', 'snarky', 'sarcastic', 'witty', 'dry', 'funny', 'serious', 'professional', 'cute', 'sexy', 'hot', 'cool', 'chill', 'laid_back', 'relaxed']

    #looks - only for pro
    ethnicity: Optional[str] = "Any"
    age: Optional[int] = None
    hair_color: Optional[str] = "Any"
    hair_style: Optional[str] = "Any"
    eyes: Optional[str] = "Any"
    skin_color: Optional[str] = "Any"
    physique: Optional[str] = "Any"


    relationship_with_user: Optional[str] = "Any"
    backstory: Optional[str] = None
    prologue: Optional[str] = None
    # others...(ykwim)

    updated_at: datetime = Field(default_factory=datetime.now)

class Bot(BaseModel):
    

    bot_details: BotDetails = Field(default_factory=BotDetails)

    # user_id: str
    # chat_id: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
