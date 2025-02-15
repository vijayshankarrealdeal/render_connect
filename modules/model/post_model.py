from sqlmodel import SQLModel

class PostOut(SQLModel):
    title: str
    content: str