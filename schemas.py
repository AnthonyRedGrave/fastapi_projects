from pydantic import BaseModel, EmailStr, constr, ValidationError, validator


class UserIn(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=8)
    password2: str


    @validator("password2")
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValidationError("passwords are not similar!")
        return v