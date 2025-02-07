from fastapi import FastAPI, Depends, HTTPException, Query
from modules.database.db import get_db
from modules.model.post_model import PostOutput
from sqlalchemy.orm import Session
from sqlalchemy import text as sql_text
from typing import List



app = FastAPI()


@app.get("/")
def first():
    return {"message": "hello"}


@app.get("/db")
def read_root(db: Session = Depends(get_db)):
    query = sql_text("SELECT ")
    result = db.execute(query).fetchone()
    return {"server_time": str(result[0])}


@app.get("/get_feed", response_model=List[PostOutput])
def get_feed(
    limit: int = Query(..., gt=0, le=100, description="Number of items to retrieve"),
    db: Session = Depends(get_db)
):
    """
    Fetches a feed of memes limited by the 'limit' parameter.
    
    - **limit**: Number of memes to retrieve (1-100)
    """
    try:
        query = sql_text(
            "SELECT * FROM meme ORDER BY RANDOM() LIMIT :limit;"
        )
        result = db.execute(query, {"limit": limit}).fetchall()
        response = [PostOutput.from_orm(row) for row in result]
        return response
    except Exception as e:
        # Log the error as needed
        raise HTTPException(status_code=500, detail="Internal Server Error")
