from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any

class ChatDetails(BaseModel):
    uid: str
    user_id: str
    bot_id: str
    chat_id: str

    rules: list[str] = []
    current_mood: str = "dominant"
    important_events: list[str] = []
    nickname: Optional[str] = None
    any_other_such_details: Dict[str, Any] = {}

