from pydantic import BaseModel, ValidationError, constr, validator


class UserIn(BaseModel):
    username: str
    password: constr(min_length=8)
    password2: str


    @validator("password2")
    def passwords_match(cls, password2, values, **kwargs):
        if 'password' in values and password2! = values['password']:
            raise ValidationError("passwords are not similar!")
        return password2


class User(BaseModel):
    id: int
    username: str
    hashed_password: str
