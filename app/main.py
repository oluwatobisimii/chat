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

chat_service = ChatService()

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
async def websocket_endpoint(websocket: WebSocket, contest_id: str, client_id: str, db: Session = Depends(get_db)):
    await manager.connect(websocket, contest_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            match message_data["type"]:
                case "message":
                    await chat_service.handle_message(db, message_data, contest_id, client_id, manager)
                case "reaction":
                    await chat_service.toggle_reaction(
                        db, message_data["message_id"], message_data["emoji"], message_data["userReaction"], contest_id, manager
                    )
    except Exception as e:
        print(f"Error: {e}")
    finally:
        manager.disconnect(websocket, contest_id)

@app.get("/messages/{contest_id}", response_model=List[MessageResponse])
def read_messages(contest_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    messages = MessageRepository.get_messages(db, contest_id, skip=skip, limit=limit)
    return messages