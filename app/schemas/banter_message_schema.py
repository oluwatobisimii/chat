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
    @classmethod
    def from_dict(cls, contest_id: str, sender_id: str, data: dict):
        return cls(
            contest_id=contest_id,
            sender_id=sender_id,
            username=data["username"],
            text=data["text"],
            avatar_color_one=data.get("avatarColorOne"),
            avatar_color_two=data.get("avatarColorTwo"),
            reply_to=data.get("replyTo"),
        )


class MessageResponse(MessageBase):
    id: int
    timestamp: datetime
    reactions: dict | None = None

    class Config:
        orm_mode = True