from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class ChatMessage(BaseModel):
    timestamp:datetime
    role: str
    content: str

class ChatDetails(BaseModel):
    rules: list[str] = Field(default_factory=list)
    current_mood: str = "dominant"
    important_events: list[str] = Field(default_factory=list)
    nickname: Optional[str] = None
    any_other_such_details: Dict[str, Any] = Field(default_factory=dict)

class Chat(BaseModel):
    user_id: str
    bot_id: str

    chat_history: list[ChatMessage] = Field(default_factory=list)
    chat_details: ChatDetails = Field(default_factory=ChatDetails)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

