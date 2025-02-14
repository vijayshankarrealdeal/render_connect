from sqlmodel import SQLModel
from datetime import datetime
class PostOutput(SQLModel):
    id: int
    name: str
    img: str
    captions: str
    download_url: str
    image_text: str
    created_at: datetime