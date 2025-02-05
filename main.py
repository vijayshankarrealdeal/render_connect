from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def first():
    return {"message": "hello"}

@app.get("/hello")
def second():
    return  {"message": "hello_test"}