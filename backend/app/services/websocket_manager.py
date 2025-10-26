from fastapi import WebSocket
from typing import Dict, Set

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.user_connections: Dict[str, str] = {}

    async def connect(self, websocket: WebSocket, conversation_id: str, user_id: str):
        await websocket.accept()
        if conversation_id not in self.active_connections:
            self.active_connections[conversation_id] = set()
        self.active_connections[conversation_id].add(websocket)
        self.user_connections[user_id] = conversation_id

    def disconnect(self, websocket: WebSocket, conversation_id: str, user_id: str):
        self.active_connections[conversation_id].discard(websocket)
        if user_id in self.user_connections:
            del self.user_connections[user_id]

    async def broadcast(self, conversation_id: str, message: dict):
        if conversation_id in self.active_connections:
            disconnected = set()
            for connection in self.active_connections[conversation_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    disconnected.add(connection)
            for connection in disconnected:
                self.active_connections[conversation_id].discard(connection)

manager = ConnectionManager()
