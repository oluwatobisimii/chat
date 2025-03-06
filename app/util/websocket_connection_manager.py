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

    def disconnect(self, websocket: WebSocket, contest_id: str):
        if contest_id in self.active_connections:
            self.active_connections[contest_id].remove(websocket)

    async def broadcast(self, contest_id: str, message: str):
        if contest_id in self.active_connections:
            for connection in self.active_connections[contest_id]:
                await connection.send_text(message)
