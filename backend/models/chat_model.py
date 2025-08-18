from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ChatMessage(BaseModel):
    timestamp:datetime
    role: str
    content: str

class Chat(BaseModel):
    user_id: str
    bot_id: str
    chat_history: list[ChatMessage] = []

