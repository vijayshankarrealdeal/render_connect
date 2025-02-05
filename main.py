from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from modules.database.db import get_db


app = FastAPI()


@app.get("/")
def first():
    return {"message": "hello"}


@app.get("/db")
def read_root(db: Session = Depends(get_db)):
    result = db.execute("SELECT now()").fetchone()
    return {"server_time": str(result[0])}
