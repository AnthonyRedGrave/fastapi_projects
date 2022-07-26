from auth_handler import decodeJWT
from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str)->str:
    return pwd_context.hash(password)

def verify_password(password: str, hash: str)->str:
    return pwd_context.verify(password, hash)


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid auth scheme")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid auth code")
        
    def verify_jwt(self, jwt_token: str)->bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwt_token)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid


# создание сообщений
# написать сообщение