from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
from app.services.websocket_manager import manager
from app.core.database import get_pool

router = APIRouter()

@router.websocket("/ws/{conversation_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, conversation_id: str, user_id: str):
    await manager.connect(websocket, conversation_id, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            try:
                pool = get_pool()
                async with pool.connection() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute("""
                            INSERT INTO messages (conversation_id, sender_id, content)
                            VALUES (%s, %s, %s)
                            RETURNING id, created_at
                        """, (conversation_id, user_id, message_data["content"]))

                        result = await cur.fetchone()
                        msg_id, created_at = result
                        await conn.commit()

                        broadcast_data = {
                            "type": "message",
                            "id": str(msg_id),
                            "conversation_id": conversation_id,
                            "sender_id": user_id,
                            "content": message_data["content"],
                            "created_at": created_at.isoformat()
                        }
                        await manager.broadcast(conversation_id, broadcast_data)
            except Exception as e:
                print(f"Error saving message: {e}")

    except WebSocketDisconnect:
        manager.disconnect(websocket, conversation_id, user_id)
        await manager.broadcast(conversation_id, {
            "type": "user_disconnected",
            "user_id": user_id
        })
