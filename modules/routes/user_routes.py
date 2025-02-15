# modules/routes/user_routes.py
from __future__ import annotations
from typing import List, Optional, Union
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from modules.engine import user
from modules.database.db import get_db
from modules.model.user_model import UserOut, UserIn  # User is the table model, UserOut is the Pydantic output model

class UserRoutes:
    def __init__(self):
        self.router = APIRouter()
        self.register_routes()
    
    def register_routes(self):
        # For a successful response, we expect a list of UserOut.
        # If there is an error (e.g., no users found), we raise an HTTPException.
        self.router.add_api_route(
            '/users', 
            self.get_users, 
            methods=['GET'],
            response_model=List[UserOut],
            responses={404: {"description": "No users found"}}, 
            status_code=status.HTTP_200_OK
        )
        self.router.add_api_route('/users', self.create_user, methods=['POST'])
        self.router.add_api_route('/users/{user_id}', self.get_user, methods=['GET'])
        self.router.add_api_route('/users/{user_id}', self.update_user, methods=['PUT'])
        self.router.add_api_route('/users/{user_id}', self.delete_user, methods=['DELETE'])
    
    async def get_users(self, username: Optional[str] = None, session: Session = Depends(get_db)) -> List[UserOut]:
        # Get users using the engine function. Make sure your engine function queries using the table model (User).
        users = user.get_users(session=session, username=username)
        return users
    
    async def create_user(self, request: UserIn) -> UserOut:
        new_user = user.create_user(request)
        return new_user
    
    async def get_user(self, user_id: int):
        return {"message": f"Get user with id {user_id}"}
    
    async def update_user(self, user_id: int):
        return {"message": f"Update user with id {user_id}"}
    
    async def delete_user(self, user_id: int):
        return {"message": f"Delete user with id {user_id}"}