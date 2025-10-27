from fastapi import APIRouter, HTTPException
from app.schemas import UserRegister, UserLogin
from app.core.security import create_access_token, hash_password
from app.core.database import get_pool

router = APIRouter()

@router.post("/register")
async def register(user: UserRegister):
    try:
        pool = get_pool()
        async with pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT id FROM users WHERE email = %s", (user.email,))
                if await cur.fetchone():
                    raise HTTPException(status_code=400, detail="Email already registered")
                await cur.execute("SELECT id FROM users WHERE username = %s", (user.username,))
                if await cur.fetchone():
                    raise HTTPException(status_code=400, detail="Username already registered")


                password_hash = hash_password(user.password)

                await cur.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s) RETURNING id",
                    (user.username, user.email, password_hash)
                )
                user_id = (await cur.fetchone())[0]
                await conn.commit()

                token = create_access_token(str(user_id))
                return {"access_token": token, "token_type": "bearer","user_id":user_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
async def login(user: UserLogin):
    try:
        pool = get_pool()
        async with pool.connection() as conn:
            async with conn.cursor() as cur:
                password_hash = hash_password(user.password)

                await cur.execute(
                    "SELECT id FROM users WHERE email = %s AND password_hash = %s RETURNING id",
                    (user.email, password_hash)
                )
                result = await cur.fetchone()
                if not result:
                    raise HTTPException(status_code=401, detail="Invalid credentials")

                user_id = result[0]
                token = create_access_token(str(user_id))
                return {"access_token": token, "token_type": "bearer","user_id":user_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
