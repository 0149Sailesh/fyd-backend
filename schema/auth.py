from pydantic import BaseModel, validator


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
        if not (len(v) == 10 and v.isdigit()):
            raise ValueError("invalid phone number")


class LoginDetails(BaseModel):
    phone_number: str
    password: str

    @validator("phone_number")
    def check_phone_number(cls, v: str):
        if not (len(v) < 10 and v.isdigit()):
            raise ValueError("invalid phone number")
