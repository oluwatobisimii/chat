import json
from app.schemas.banter_message_schema import MessageCreate
from app.repositories.banter_message_repository import MessageRepository
from sqlalchemy.orm import Session
from app.util.websocket_connection_manager import ConnectionManager


class ChatService:
    @staticmethod
    def send_message(db, message_data: MessageCreate):
        return MessageRepository.create_message(db, message_data)

    # @staticmethod
    # def toggle_reaction(db, message_id: int, emoji: str, user_reaction: dict):
    #     return MessageRepository.update_reactions(db, message_id, emoji, user_reaction)
    
    @staticmethod
    async def toggle_reaction(db: Session, message_id: int, emoji: str, user_reaction: dict, manager: ConnectionManager):
        updated_message = await MessageRepository.update_reactions(db, message_id, emoji, user_reaction)
        if not updated_message:
            return None

        # Broadcast the updated message to all connected clients
        contest_id = updated_message.contest_id
        await manager.broadcast(
            contest_id,
            json.dumps(
                {
                    "id": updated_message.id,
                    "sender_id": updated_message.sender_id,
                    "username": updated_message.username,
                    "text": updated_message.text,
                    "timestamp": updated_message.timestamp.isoformat(),
                    "reactions": updated_message.reactions or {},
                    "replyTo": updated_message.reply_to,
                        'avatar_color_one': updated_message.avatar_color_one,
                        'avatar_color_two': updated_message.avatar_color_two,
                }
            ),
        )

        return updated_message