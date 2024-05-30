from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from typing import Optional
from src.lib.validator import users as users_validator
from src.lib.domain import users as users_domain
# Import fast api status code
from fastapi import status


router = APIRouter()

@router.get("/users/{user_id}", tags=["Users"])
def get_user(user_id: str, request: Request):
    return JSONResponse(content={"error": "User not found"}, status_code=status.HTTP_404_NOT_FOUND)
    # result = users_domain.get_user(user_id=user_id)
    # if not result:
    #     return JSONResponse(content={"error": "User not found"}, status_code=404)
    # return JSONResponse(content=result, status_code=200)

@router.post("/users", tags=["Users"])
def create_user(msg: users_validator.CreateUser, request: Request):
    result = users_domain.create_user(**msg.dict())
    return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
