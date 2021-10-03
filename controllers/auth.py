from app.db import engine
from model.user import UserModel
from fastapi import HTTPException


from routes.auth import RegistrationDetails, LoginDetails
from utils.auth import auth_hanlder


async def register_user(user: RegistrationDetails):
    # checking if user already exist
    user_instance = await engine.find_one(UserModel, UserModel.phone_number == user.phone_number)
    if not user_instance:
        raise HTTPException(
            status_code=400, detail="phonenumber already exist")
    # creating new user instance
    user_instance = UserModel(name=user.name, password=auth_hanlder.get_password_hash(
        user.password), phone_number=user.phone_number)
    # saving new user in db
    saved_user = await engine.save(user_instance)

    if saved_user == None:
        raise HTTPException(
            status_code=500, detail="something went wrong, try again later")

    return saved_user


async def login_user(creds: LoginDetails):
    user = None
    user = await engine.find_one(UserModel, UserModel.phone_number == creds.phone_number)

    if user is None or not (auth_hanlder.verify_password(creds.password, user.password)):
        raise HTTPException(
            status_code=401, detail="Invalid phonenumber and password")

    return auth_hanlder.encode_token(user.id)
