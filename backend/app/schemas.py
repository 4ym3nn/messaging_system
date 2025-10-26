from pydantic import BaseModel
from datetime import datetime
from typing import List

# User Schemas
class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    avatar_url: str | None
    status: str

# Message Schemas
class MessageCreate(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    sender_id: str
    content: str
    created_at: datetime

# Conversation Schemas
class ConversationResponse(BaseModel):
    id: str
    name: str | None
    is_group: bool
    members: List[UserResponse]
    last_message: MessageResponse | None
