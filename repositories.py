from db import User
from schemas import UserIn
from core.security import hash_password


class UserRepository:
    async def create(self, u: UserIn) -> User:
        user = await User.objects.create(name=u.name, email = u.email, hashed_password= hash_password(u.password))
        return u
