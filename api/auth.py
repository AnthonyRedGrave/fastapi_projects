from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


# response_model = Token
# status_code = 201

@router.post('/register')
def register():
    #user_data = UserIn
    #auth_service Depends()
    pass