from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message):
        print(self.active_connections)
        for connection in self.active_connections:
            print(message)
            await connection.send_text(message)

manager = ConnectionManager()

router = APIRouter(
  tags=["Websockets"]
)

@router.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
          await websocket.receive_text()
          # await websocket.send_text(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
