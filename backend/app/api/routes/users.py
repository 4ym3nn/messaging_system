from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas import UserResponse
from app.core.security import verify_token
from app.core.database import get_pool

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_current_user(user_id: str = Depends(verify_token)):
    try:
        pool = get_pool()
        async with pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT id, username, email, avatar_url, status FROM users WHERE id = %s",
                    (user_id,)
                )
                row = await cur.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail="User not found")
                return {
                    "id": str(row[0]),
                    "username": row[1],
                    "email": row[2],
                    "avatar_url": row[3],
                    "status": row[4]
                }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[UserResponse])
async def get_all_users(user_id: str = Depends(verify_token)):
    try:
        pool = get_pool()
        async with pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT id, username, email, avatar_url, status FROM users WHERE id != %s",
                    (user_id,)
                )
                rows = await cur.fetchall()
                return [
                    {
                        "id": str(row[0]),
                        "username": row[1],
                        "email": row[2],
                        "avatar_url": row[3],
                        "status": row[4]
                    }
                    for row in rows
                ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
