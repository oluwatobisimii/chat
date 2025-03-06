from fastapi.websockets import WebSocket

class WebSocketManager:
    def __init__(self):
        self.connected_clients = []
    
    async def connect(self, websocket: WebSocket):

        client_ip = f"{websocket.client.host}:{websocket.client.port}"

        await websocket.accept()
        print(f"client {websocket.client.host}: {websocket.client.port} connected")

        # add client to list of connected clients
        self.connected_clients.append(websocket)
        print(f"connected clients: {self.connected_clients}")

        # send welmcome message to client
        message = {"client": client_ip,
                   "message": f"Welcome {client_ip}"}  
        await websocket.send_json(message)


    async def send_message(self, websocket: WebSocket, message: dict):
        message = {
        'client': f"client {websocket.client.host}: {websocket.client.port}",
        "message": message }
        await websocket.send_json(message)


    async def disconnect(self, websocket: WebSocket):
        print(f"client {websocket.client.host}: {websocket.client.port} disconnected")
        self.connected_clients.remove(websocket)
        print(f"connected clients: {self.connected_clients}")