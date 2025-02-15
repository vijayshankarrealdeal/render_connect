from typing import Optional
from sqlmodel import Field, SQLModel

class UserOut(SQLModel):
    username: str
    email: str
    bio: str
    profile_picture_url: str
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)

class UserIn(SQLModel):
    user_id: int
    username: str
    email: str
    password: str
    bio: str
    profile_picture_url: str