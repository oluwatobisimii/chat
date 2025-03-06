from pydantic import BaseModel
from datetime import datetime


class MessageBase(BaseModel):
    contest_id: str
    sender_id: str
    username: str
    avatar_color_one: str | None = None
    avatar_color_two: str | None = None
    text: str
    reply_to: int | None = None


class MessageCreate(MessageBase):
    pass


class MessageResponse(MessageBase):
    id: int
    timestamp: datetime
    reactions: dict | None = None

    class Config:
        orm_mode = True