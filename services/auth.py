from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.hash import bcrypt
from pydantic import ValidationError
from schemas.users import User, UserIn
from schemas.tokens import Token
from db import User as UserDB


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in')


class AuthService:

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password:str)->bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password:str)->str:
        return bcrypt.hash(password)

    @classmethod
    def verify_token(cls, token:str) -> User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
        try:
            payload = jwt.decode(
                token,
                str,
                algorithms=['HS256']
            )
        except JWTError:
            raise exception from None
        
        user_data = payload.get('user')

        try:
            user = User.parse_obj(user_data)
        except ValidationError:
            raise exception from None
        return user

    @classmethod
    def create_token(cls, user: UserDB) -> Token:
        user_data = User.from_orm(user) # user - сохраненная запись юзера из бд
        print("USER DATA FROM ORM", user_data)
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=3600),
            'sub': str(user_data.id),
            'user': 

        }

    def register_new_user(self, user_data: UserIn)-> Token:
        user = UserDB.objects.create(username = user_data.username, hashed_password = self.hash_password(user_data.password))
        return self.create_token(user)
