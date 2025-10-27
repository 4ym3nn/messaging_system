from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas import ConversationResponse,ConversationCreate
from app.core.security import verify_token
from app.core.database import get_pool

router = APIRouter()

@router.post("")
async def create_conversation(body:ConversationCreate,user_id: str = Depends(verify_token)):
    try:
        pool = get_pool()
        async with pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO conversations (is_group,name) VALUES (%s,%s) RETURNING id",
                    (body.is_group,body.name)
                )
                conv_id = (await cur.fetchone())[0]

                await cur.execute(
                    "INSERT INTO conversation_members (conversation_id, user_id) VALUES (%s, %s)",
                    (conv_id, user_id)
                )
                if body.is_group :
                    for member_id in body.member_ids:
                        await cur.execute(
                            "INSERT INTO conversation_members (conversation_id, user_id) VALUES (%s, %s)",
                            (conv_id, member_id)
                        )
                else :
                    await cur.execute(
                        "INSERT INTO conversation_members (conversation_id, user_id) VALUES (%s, %s)",
                        (conv_id, body.member_ids[0])
                    )


                await conn.commit()

                return {"id": str(conv_id), "is_group": False}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{conversation_id}/members/{member_id}")
async def add_member(conversation_id: str, member_id: str, user_id: str = Depends(verify_token)):
    try:
        pool = get_pool()
        async with pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO conversation_members (conversation_id, user_id) VALUES (%s, %s)",
                    (conversation_id, member_id)
                )
                await conn.commit()
                return {"status": "member added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[ConversationResponse])
async def get_conversations(user_id: str = Depends(verify_token)):
    try:
        pool = get_pool()
        async with pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    SELECT DISTINCT ON (c.id) c.id, c.name, c.is_group
                    FROM conversations c
                    JOIN conversation_members cm ON c.id = cm.conversation_id
                    WHERE cm.user_id = %s
                    ORDER BY c.id, c.updated_at DESC
                """, (user_id,))

                conversations = []
                for row in await cur.fetchall():
                    conv_id, name, is_group = row

                    await cur.execute("""
                        SELECT u.id, u.username, u.email, u.avatar_url, u.status
                        FROM users u
                        JOIN conversation_members cm ON u.id = cm.user_id
                        WHERE cm.conversation_id = %s
                    """, (conv_id,))

                    members = [
                        {
                            "id": str(m[0]),
                            "username": m[1],
                            "email": m[2],
                            "avatar_url": m[3],
                            "status": m[4]
                        }
                        for m in await cur.fetchall()
                    ]

                    await cur.execute("""
                        SELECT id, conversation_id, sender_id, content, created_at
                        FROM messages
                        WHERE conversation_id = %s
                        ORDER BY created_at DESC
                        LIMIT 1
                    """, (conv_id,))

                    last_msg = await cur.fetchone()
                    last_message = None
                    if last_msg:
                        last_message = {
                            "id": str(last_msg[0]),
                            "conversation_id": str(last_msg[1]),
                            "sender_id": str(last_msg[2]),
                            "content": last_msg[3],
                            "created_at": last_msg[4]
                        }

                    conversations.append({
                        "id": str(conv_id),
                        "name": name,
                        "is_group": is_group,
                        "members": members,
                        "last_message": last_message
                    })

                return conversations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
