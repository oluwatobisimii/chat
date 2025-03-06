import json
from fastapi import WebSocket

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, contest_id: str):
        await websocket.accept()
        if contest_id not in self.active_connections:
            self.active_connections[contest_id] = []
        self.active_connections[contest_id].append(websocket)
        print(self.active_connections)

    def disconnect(self, websocket: WebSocket, contest_id: str):
        if contest_id in self.active_connections:
            self.active_connections[contest_id].remove(websocket)

    async def broadcast(self, contest_id: str, message: str):
        
        if isinstance(message, dict):
                message_payload = json.dumps(message)
        
        else: 
            message_payload = json.dumps({
                "id": message.id,
                "sender_id": message.sender_id,
                "username": message.username,
                "text": message.text,
                "timestamp": message.timestamp.isoformat(),
                "reactions": message.reactions or {},
                "replyTo": message.reply_to,
                "avatar_color_one": message.avatar_color_one,
                "avatar_color_two": message.avatar_color_two,
            })

        
        if contest_id in self.active_connections:
            for connection in self.active_connections[contest_id]:
                await connection.send_text(message_payload)
                print("Message sent!")
