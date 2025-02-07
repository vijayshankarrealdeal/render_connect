from pydantic import BaseModel
from datetime import datetime
class PostOutput(BaseModel):
    id: int
    name: str
    img: str
    captions: str
    download_url: str
    image_text: str
    created_at: datetime