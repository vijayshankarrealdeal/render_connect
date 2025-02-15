from sqlmodel import Session, text
from fastapi import HTTPException
from modules.model.user_model import UserIn, UserOut

def get_users(session: Session, username: str = None):
    query = text(f"SELECT * FROM users where username = {username}")
    users = session.exec(query).all()
    if len(users) > 1:
        return users
    raise HTTPException(status_code=404, detail="No users found")

def create_user(payload:UserIn) -> UserOut:
    print(payload)
    return payload

