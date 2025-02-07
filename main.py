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
    query = sql_text("SELECT now()")
    result = db.execute(query).fetchone()
    return {"server_time": str(result[0])}

@app.get("/create_table")
def create_table(query: str, db: Session = Depends(get_db)):
    query = sql_text(query)
    result = db.execute(query).fetchone()
    return {"res":result}

