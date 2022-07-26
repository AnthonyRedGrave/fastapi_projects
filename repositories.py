from fastapi import Depends, HTTPException, Request
from fastapi import status
from ormar import NoMatch
from pydantic import ValidationError
from db import Message, User, Chat
from schemas import UserIn, ChatIn, MessageIn
from core.security import hash_password


class UserRepository:
    async def search(self, username):
        return await User.objects.all(name__icontains=username)

    async def create(self, u: UserIn) -> User:
        exp = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this name already exists!") 
        if await User.objects.filter(name=u.name).count() > 0:
            raise exp
        await User.objects.create(name=u.name, email = u.email, hashed_password= hash_password(u.password))
        return u


async def iterate_queryset(model, emails):
    for email in emails:
        yield await model.objects.get(email=email)


class ChatRepository:
    async def create(self, c: ChatIn):
        # print(c.users)
        # print(await User.objects.filter(name__in=c.users).all())
        exp = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not all emails exist!") 
        if await c.users[0].count() != len(c.users[1]):
            raise exp
        
        new_chat = await Chat.objects.create()

        generator = iterate_queryset(User, c.users[1])
        async for user in generator:
            await new_chat.users.add(user)
        return new_chat


    async def messages(self):
        return await Message.objects.all()


    async def create_message(self, m: MessageIn, current_user):
        try:
            chat = await m.chat
            return await Message.objects.create(text = m.text, user=current_user, chat=chat)
        except NoMatch:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Chat does not exist!")

    async def read_all(self):
        return await Chat.objects.select_related("users").all()
