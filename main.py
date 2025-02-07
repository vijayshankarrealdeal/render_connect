from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from modules.database.db import get_db
from sqlalchemy import text as sql_text


app = FastAPI()


@app.get("/")
def first():
    return {"message": "hello"}


@app.get("/db")
def read_root(db: Session = Depends(get_db)):
    query = sql_text("SELECT ")
    result = db.execute(query).fetchone()
    return {"server_time": str(result[0])}


@app.post("/get_feed")
def create_table(limit:int, db: Session = Depends(get_db)):
    query = sql_text(
        f"""SELECT *
            FROM your_table
            ORDER BY RANDOM()
            LIMIT {limit};
        """
    )
    result = db.execute(query).fetchone()
    return {"payload": result}
