from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas import MessageResponse
from app.core.security import verify_token
from app.core.database import get_pool

router = APIRouter()

@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(conversation_id: str, user_id: str = Depends(verify_token)):
    try:
        pool = get_pool()
        async with pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    SELECT id, conversation_id, sender_id, content, created_at
                    FROM messages
                    WHERE conversation_id = %s
                    ORDER BY created_at ASC
                    LIMIT 50
                """, (conversation_id,))

                messages = []
                for row in await cur.fetchall():
                    messages.append({
                        "id": str(row[0]),
                        "conversation_id": str(row[1]),
                        "sender_id": str(row[2]),
                        "content": row[3],
                        "created_at": row[4]
                    })

                return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
