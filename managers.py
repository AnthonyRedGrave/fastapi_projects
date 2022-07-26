from collections import defaultdict
import re
from typing import List
from fastapi import WebSocket
from db import Message, Chat, User
from schemas import ChatSchema, MessageSchema
import json
from pydantic import parse_obj_as, parse_raw_as

def wrapper(type, data):
    return {
        "type": type,
        "data": data
    }

class ConnectionManager:
    def __init__(self) -> None:
        self.connections: dict = defaultdict(dict)


    async def connect(self, websocket: WebSocket, room_id: str):
        print("подключился")
        await websocket.accept()
        if self.connections[room_id] == {} or self.connections[room_id] == []:
            self.connections[room_id] = []
        self.connections[room_id].append(websocket)
        print(f"Connections: {self.connections[room_id]}")
        

    async def get_messages(self, chat_id):
        chat = await Chat.objects.filter(id=int(chat_id)).get()
        messages = await chat.messages.select_related("user").all()
        messages_schema = [MessageSchema(**m.dict()).dict() for m in messages]

        return messages_schema

    async def create_message(self, data):
        chat = await Chat.objects.filter(id=int(data['room_id'])).get()
        user = await User.objects.filter(email = data['email']).get()
        return await Message.objects.create(text=data['text'], chat=chat, user = user)

    async def _notify(self, data, room_id):
        for ws in self.connections[room_id]:
            await ws.send_text(json.dumps(wrapper(type="notify", data = MessageSchema(**data.dict()).dict())))

    async def send_messages(self, messages, room_id):
        for ws in self.connections[room_id]:
            await ws.send_text(json.dumps(wrapper(type="messages", data=messages)))

    def get_members(self, room_id):
        try:
            return self.connections[room_id]
        except Exception:
            return None

    def remove(self, websocket: WebSocket, room_id: str):
        self.connections[room_id].remove(websocket)
        print(f"CONNECTION {websocket} REMOVED!")


async def find_email_in_chats(email, chats):
    res_chats = []    
    for chat in chats:
        users = []
        for user in ChatSchema(**chat.dict()).dict()['users']:
            users.append(user['email'])
        if email in users:
            res_chats.append(ChatSchema(**chat.dict()).dict())
    return res_chats


async def chat_user_emails(chat):
    users = []
    for user in ChatSchema(**chat.dict()).dict()['users']:
        users.append(user['email'])
    
    return users


class ChatsManager:

    def __init__(self) -> None:
        self.connections: list = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        user_email = json.loads(await websocket.receive_text())
        if self.connections == []:
            websocket_user = {'websocket': websocket,
                              'user_email': user_email['email']
            }
            self.connections.append(websocket_user)
        return user_email


    async def get_chats(self, user_email):
        # найти только те чаты, в которых находиться юзер
        chats_db = await Chat.objects.select_related("users").all()
        chats = await find_email_in_chats(user_email['email'], chats_db)
        return wrapper(type="chats", data=chats)
    

    async def _notify_about_new_message(self, data):
        print("УВЕДОМЛЕНИЯ ДЛЯ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ!", data)
        chat = await Chat.objects.filter(id=int(data['room_id'])).select_related("users").get()
        users = await chat_user_emails(chat)
        for d in self.connections:
            if d['user_email'] in users:
                await d['websocket'].send_text(json.dumps(wrapper(type="notify_new_message", data=data)))


    def remove(self, websocket: WebSocket):
        # self.connections.remove(websocket)
        for d in self.connections:
            if d['websocket'] == websocket:
                self.connections.remove(d)
        print(f"CONNECTION {websocket} REMOVED!")
