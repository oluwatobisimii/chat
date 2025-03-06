import json
from sqlalchemy.orm import Session
from app.models.banter_message_model import Message
from app.schemas.banter_message_schema import MessageCreate
from app.models.banter_message_model import Message as BanterMessage


class MessageRepository:
    @staticmethod
    def get_messages(db: Session, contest_id: str, skip: int = 0, limit: int = 100):
        return (
            db.query(Message)
            .filter(Message.contest_id == contest_id)
            .order_by(Message.timestamp.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

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


        db_message = db.query(Message).filter(Message.id == message_id).first()
        if not db_message:
            return None

        reactions = db_message.reactions or {}
        if emoji in reactions:
            if user_reaction in reactions[emoji]:
                reactions[emoji].remove(user_reaction)
                if not reactions[emoji]:
                    del reactions[emoji]
            else:
                reactions[emoji].append(user_reaction)
        else:
            reactions[emoji] = [user_reaction]

        db_message.reactions = reactions
        db.commit()
        db.refresh(db_message)
        return db_message
    
    @staticmethod
    async def update_reactions(db: Session, message_id: int, emoji: str, user_reaction: dict):
        # Fetch the message from the database
        db_message = db.get(BanterMessage, message_id)
        if not db_message:
            return None  # Message not found

        # Initialize reactions dictionary if it doesn't exist
        reactions = json.loads(db_message.reactions) or {}

        # Check if the emoji already exists in reactions
        if emoji in reactions:
        # If the UUID already exists, remove it
            reactions[emoji] = [
            r for r in reactions[emoji] if r['uuid'] != user_reaction['uuid']
        ]
        # If no reactions are left for this emoji, delete the emoji key
        if not reactions[emoji]:
            del reactions[emoji]
            print(reactions)
        else:
         # If the emoji doesn't exist, create a new list with the user reaction
         reactions[emoji] = [user_reaction]

        # If the UUID was not removed (i.e., it didn't exist), add it
        if emoji in reactions and user_reaction['uuid'] not in [r['uuid'] for r in reactions[emoji]]:
            reactions[emoji].append(user_reaction)

        # Update the message's reactions in the database
        db_message.reactions = json.dumps(reactions)

        db.commit()
        db.refresh(db_message)
        

        return db_message