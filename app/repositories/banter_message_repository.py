import json
from sqlalchemy.orm import Session
from app.models.banter_message_model import Message
from app.schemas.banter_message_schema import MessageCreate
from app.models.banter_message_model import Message as BanterMessage


class MessageRepository:
    @staticmethod
    def get_messages(db: Session, contest_id: str, skip: int = 0, limit: int = 100):
        messages = (
            db.query(Message)
            .filter(Message.contest_id == contest_id)
            .order_by(Message.timestamp.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        
        for msg in messages:
            if isinstance(msg.reactions, str): 
                msg.reactions = json.loads(msg.reactions)

        return messages

    @staticmethod
    def create_message(db: Session, message: MessageCreate):
        db_message = Message(
            contest_id=message.contest_id,
            sender_id=message.sender_id,
            username=message.username,
            avatar_color_one=message.avatar_color_one,
            avatar_color_two=message.avatar_color_two,
            text=message.text,
            reply_to=message.reply_to,
            reactions={},
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message


    
    @staticmethod
    async def update_reactions(db: Session, message_id: int, emoji: str, user_reaction: dict):
        
        db_message = db.get(BanterMessage, message_id)
        if not db_message:
            return None 
        
        reactions = json.loads(db_message.reactions) if db_message.reactions else {}

        
        if emoji in reactions:
            reactions[emoji] = [reaction for reaction in reactions[emoji] if reaction['uuid'] != user_reaction['uuid']]
            if not reactions[emoji]:  
                del reactions[emoji]

        
        elif emoji not in reactions:
            reactions[emoji] = [user_reaction] 
            print(reactions)
        elif user_reaction['uuid'] not in [r['uuid'] for r in reactions[emoji]]:
            reactions[emoji].append(user_reaction)

        
        db_message.reactions = json.dumps(reactions)
        db.commit()
        db.refresh(db_message)
        db_message.reactions = json.loads(db_message.reactions)
        return db_message
