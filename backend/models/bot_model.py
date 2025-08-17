from pydantic import BaseModel, EmailStr
from typing import Optional, Literal

class Bot(BaseModel):
    uid: str
    name: str
    picture: Optional[str] = None
    likings: list[str] = []  # pro at these things
    behaviour: Literal['soft', 'between_soft_and_hard', 'hard', 'ease_into_it']

    #looks - only for pro
    ethnicity: Optional[str] = "Any"
    hairs: Optional[str] = "Any"
    eyes: Optional[str] = "Any"
    skin_color: Optional[str] = "Any"
    physique: Optional[str] = "Any"
    # others...(ykwim)

    user_id: str
