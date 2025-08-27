from bson.objectid import ObjectId
from mongo import db
from models.chat_model import Chat, ChatMessage
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from zoneinfo import ZoneInfo


chat_collection = db['chats']
bot_collection = db['bots']




def append_messages(chat_id: str, messages: list[dict]) -> int:
    validated = []
    for msg in messages:
        # normalize timestamp
        ts = msg.get("timestamp")
        if isinstance(ts, datetime):
            pass
        elif isinstance(ts, str):
            parsed = None
            # try RFC2822/HTTP-date
            try:
                parsed = parsedate_to_datetime(ts)
            except Exception:
                parsed = None
            # try ISO format
            if parsed is None:
                try:
                    parsed = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                except Exception:
                    parsed = None
            msg["timestamp"] = parsed or datetime.utcnow()
        else:
            msg["timestamp"] = datetime.utcnow()

        validated.append(ChatMessage(**msg).model_dump())
    res = chat_collection.update_one({"_id": ObjectId(chat_id)}, {"$push": {"chat_history": {"$each": validated}}, "$set": {"updated_at": datetime.now()}})
    return res.modified_count

def get_latest_user_messages(messages: list[dict]) -> list[dict]:
    last_assistant_index = -1
    for idx in range(len(messages) - 1, -1, -1):
        try:
            if isinstance(messages[idx], dict) and messages[idx].get('role') == 'assistant':
                last_assistant_index = idx
                break
        except Exception:
            continue

    pending = messages[last_assistant_index + 1:] if last_assistant_index >= 0 else messages
    new_user_messages = [m for m in pending if isinstance(m, dict) and m.get('role') == 'user']

    # prepend timestamp to each message in the format of YYYY-MM-DD HH:MM:SS. Form frontend, timestamp is sent as follows - timestamp: new Date().toISOString()
    # for msg in new_user_messages:
    #     msg['content'] = f"<timestamp>{msg['timestamp']}</timestamp>\n{msg['content']}"
    


    return new_user_messages





def get_current_time(user_timezone: str):
    # get current time in UTC
    now_utc = datetime.now(timezone.utc)
    
    # convert to user's timezone
    now_local = now_utc.astimezone(ZoneInfo(user_timezone))
    
    # format like JS new Date().toString()
    return now_local.strftime("%a %b %d %Y %H:%M:%S GMT%z (%Z)")