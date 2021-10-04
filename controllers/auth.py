from fastapi import HTTPException
from model.user import User

from schema.auth import RegistrationDetails, LoginDetails
from utils.auth import auth_hanlder


def register_user(user: RegistrationDetails):
    # checking if user already exist
    try:
        user_instance = User.objects.get(phone_number=user.phone_number)
    except User.DoesNotExist:

        user_instance = User()
        user_instance.name = user.name
        user_instance.phone_number = user.phone_number
        user_instance.password = auth_hanlder.get_password_hash(user.password)

        # saving new user in db
        user_instance.save()

        return user_instance
    else:
        raise HTTPException(
            status_code=400, detail="phonenumber already exist")


def login_user(creds: LoginDetails):
    try:
        user = User.objects.get(phone_number=creds.phone_number)
    except User.DoesNotExist:
        raise HTTPException(
            status_code=401, detail="Invalid phonenumber and password")

    return auth_hanlder.encode_token(user.id)
