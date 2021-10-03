from typing import Optional
from fastapi import APIRouter
from fastapi.param_functions import Depends
from pydantic import BaseModel, validator

from controllers.auth import register_user, login_user
from model.user import UserModel
from utils.auth import auth_hanlder
from app.db import engine
from schema.auth import RegistrationDetails, LoginDetails

router = APIRouter()


@router.post("/register", response_description="user registration successful")
async def register(user: RegistrationDetails):
    saved_user = await register_user(user)
    print(saved_user)
    return {"user": saved_user, "message": "Registration successfull"}


@router.post("/login", response_description="jwt token")
async def login(creds: LoginDetails):
    token = await login_user(creds)

    return {"token": token, "message": "Login successfull"}


@router.get("/me", response_description="authenticated user")
async def getUser(user_id=Depends(auth_hanlder.auth_wrapper)):
    user = await engine.find_one(UserModel, UserModel.id == user_id)
    return {"user": user, "is_authenticated": True}
