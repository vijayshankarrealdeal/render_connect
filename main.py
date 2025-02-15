from fastapi import FastAPI
from modules.routes.user_routes import UserRoutes



app = FastAPI()

user_routes = UserRoutes()
app.include_router(user_routes.router, prefix="/api")