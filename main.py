from auth_handler import decodeJWT
from core.security import JWTBearer
from fastapi import HTTPException, Query, Request, status
from fastapi_jwt_auth import AuthJWT
from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from db import database
from endpoints import router
from managers import ChatsManager, ConnectionManager
from fastapi.middleware.cors import CORSMiddleware
import json
from websockets.exceptions import ConnectionClosedOK
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
# websockets.exceptions.ConnectionClosedOK

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]


app = FastAPI()

app.include_router(router, prefix='/api', tags=['users'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"

@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


manager = ConnectionManager()
chats_manager = ChatsManager()


@app.websocket("/ws")
async def chats_websockets_endpoint(websocket: WebSocket, token: str = Query(...)):
    email = await chats_manager.connect(websocket)
    payload = decodeJWT(token)
    if payload is None:
        await websocket.send_text(json.dumps({"status": status.HTTP_401_UNAUTHORIZED,
                                              "detail": "Auth error!"
        }))
        chats_manager.remove(websocket)
        return

    try:
        # print("ЖДУ ПОЛЬЗОВАТЕЛЯ")
        # data = await websocket.receive_text()
        while True:
            print("ИЩУ ЧАТЫ!")
            chats = await chats_manager.get_chats(email)
            await websocket.send_text(json.dumps(chats))
            print("ОТПРАВИЛ ЧАТЫ!")
            print("ЖДУ УВЕДОМЛЕНИЯ ОТ ПОЛЬЗОВАТЕЛЯ!")
            await websocket.receive_text()

    except (WebSocketDisconnect, ConnectionClosedOK, HTTPException):
        print("ВЫШЕЛ!")
        chats_manager.remove(websocket)


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id):
    await manager.connect(websocket, room_id)
    try:
        print("НАЧИНАЮ СКАЧИВАТЬ СООБЩЕНИЯ")
        messages = await manager.get_messages(chat_id=room_id)
        await manager.send_messages(messages, room_id)
        
        while True:
            print("ЖДУ СООБЩЕНИЯ!")
            await websocket.send_text(json.dumps(messages))

            data = await websocket.receive_text()
            d = json.loads(data)
            d['room_id'] = room_id
            await chats_manager._notify_about_new_message(d)

            new_message = await manager.create_message(data=d)

            room_members = (
                manager.get_members(room_id)
                if manager.get_members(room_id) is not None
                else []
            )
            if websocket not in room_members:
                print("SENDER NOT IN CHAT MEMBERS: RECCONNECTING")
            await manager._notify(new_message, room_id)
            # break
    except (WebSocketDisconnect, ConnectionClosedOK):
        print("ВЫШЕЛ!")
        manager.remove(websocket, room_id)

    


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()

@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


@app.get('/')
async def root():
    return {'1':'2'}



