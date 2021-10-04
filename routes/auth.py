from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
import json

from controllers.auth import register_user, login_user
from model.user import User
from utils.auth import auth_hanlder
from schema.auth import RegistrationDetails, LoginDetails

router = APIRouter()


@router.post("/register", response_description="user registration successful")
def register(user: RegistrationDetails):
    print(user)

    saved_user = register_user(user)
    print(saved_user)
    print(type(saved_user))
    return {"user": json.loads(saved_user.to_json()), "message": "Registration successfull"}


@router.post("/login", response_description="jwt token")
def login(creds: LoginDetails):
    token = login_user(creds)
    print(token)
    return {"token": token, "message": "Login successfull"}


@router.get("/me", response_description="authenticated user")
async def getUser(user_id=Depends(auth_hanlder.auth_wrapper)):
    try:
        user = User.objects.get(phone_number=user_id)
    except User.DoesNotExist:
        raise HTTPException(
            status_code=404, detail="user not found")

    return {"user": json.loads(user.to_json()), "is_authenticated": True}
