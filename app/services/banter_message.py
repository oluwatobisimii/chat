import json
from app.schemas.banter_message_schema import MessageCreate
from app.repositories.banter_message_repository import MessageRepository
from sqlalchemy.orm import Session
from app.util.websocket_connection_manager import ConnectionManager


class ChatService:
    
    def send_message(self, db: Session, message_data: MessageCreate):
        new_message = MessageRepository.create_message(db, message_data)
        return new_message

    
    async def handle_message(self, db: Session, message_data: dict, contest_id: str, client_id: str, manager):
        message_create = MessageCreate.from_dict(contest_id, client_id, message_data)

        new_message = self.send_message(db, message_create)

        await manager.broadcast(contest_id, new_message)

    
    
    async def toggle_reaction(self, db: Session, message_id: int, emoji: str, user_reaction: dict, contest_id: str, manager: ConnectionManager):
        updated_message = await MessageRepository.update_reactions(db, message_id, emoji, user_reaction)
        if not updated_message:
            return None
        

        await manager.broadcast(
            contest_id,
            updated_message
        )

        return updated_message