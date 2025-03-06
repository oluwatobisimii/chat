from fastapi import FastAPI, WebSocket, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import json

from app.models.banter_message_model import Base, Message
from app.schemas.banter_message_schema import MessageCreate, MessageResponse
from app.repositories.banter_message_repository import MessageRepository
from app.database import get_db

from app.services.banter_message import ChatService
from app.database import engine
from app.util.websocket_connection_manager import ConnectionManager

app = FastAPI()

# Configure CORS
origins = ["*", "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables in the database
Base.metadata.create_all(bind=engine)



manager = ConnectionManager()



@app.websocket("/ws/{contest_id}/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket, contest_id: str, client_id: str, db: Session = Depends(get_db)
):
    await manager.connect(websocket, contest_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            
            message_create = MessageCreate(
                    contest_id=contest_id,
                    sender_id=client_id,
                    username=message_data["username"],
                    avatar_color_one=message_data.get("avatarColorOne"),
                    avatar_color_two=message_data.get("avatarColorTwo"),
                    text=message_data["text"],
                    reply_to=message_data.get("replyTo"),
                )
            new_message = ChatService.send_message(db, message_create)
            print(new_message)
            await manager.broadcast(
                    contest_id,
                    json.dumps(
                        {
                            "id": new_message.id,
                            "sender_id": new_message.sender_id,
                            "username": new_message.username,
                            "text": new_message.text,
                            "timestamp": new_message.timestamp.isoformat(),
                            "reactions": new_message.reactions or {},
                            "replyTo": new_message.reply_to,
                            'avatar_color_one': new_message.avatar_color_one,
                        'avatar_color_two': new_message.avatar_color_two,
                        }
                    ),
                )
    except Exception as e:
        print(f"Error: {e}")
    finally:
        manager.disconnect(websocket, contest_id)

@app.get("/messages/{contest_id}", response_model=List[MessageResponse])
def read_messages(contest_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    messages = MessageRepository.get_messages(db, contest_id, skip=skip, limit=limit)
    return messages




@app.post("/messages/{message_id}/toggle-reaction")
async def toggle_reaction(
    message_id: int, db: Session = Depends(get_db), 
    reaction_data: dict = Body(...),
    ):
    emoji = reaction_data.get('emoji')
    user_reaction = reaction_data.get('userReaction')
    updated_message = await ChatService.toggle_reaction(db, message_id, emoji, user_reaction, manager)
    if not updated_message:
        raise HTTPException(status_code=404, detail="Message not found")
    return updated_message