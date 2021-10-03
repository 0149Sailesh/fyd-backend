from typing import Optional
from fastapi import APIRouter
from fastapi.param_functions import Depends
from pydantic import BaseModel, validator

from controllers.auth import register_user, login_user
from model.user import UserModel
from utils.auth import auth_hanlder
from app.db import engine

router = APIRouter()


class RegistrationDetails(BaseModel):
    name: str
    password: str
    repeat_password: str
    phone_number: str

    # Check if password is at least 6 characters long
    @validator("password")
    def check_password_length(cls, v):
        if len(v) < 5:
            raise ValueError("password is short")
        return v

    # check if password and repeat_password match
    @validator("repeat_password")
    def check_password_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords do not match")
        return v

    @validator("phone_number")
    def check_phone_number(cls, v: str):
        if not (len(v) < 10 and v.isdigit()):
            raise ValueError("invalid phone number")


class LoginDetails(BaseModel):
    phone_number: str
    password: str

    @validator("phone_number")
    def check_phone_number(cls, v: str):
        if not (len(v) < 10 and v.isdigit()):
            raise ValueError("invalid phone number")


@router.post("/register", response_description="user registration successful")
def register(user: RegistrationDetails):
    saved_user = register_user(user)

    return {"user": saved_user, "message": "Tegistration successfull"}


@router.post("/login", response_description="jwt token")
def login(creds: LoginDetails):
    token = login_user(creds)

    return {"token": token, "message": "Login successfull"}


@router.get("/me", response_description="authenticated user")
async def getUser(user_id=Depends(auth_hanlder.auth_wrapper)):
    return await engine.find_one(UserModel, UserModel.id == user_id)
