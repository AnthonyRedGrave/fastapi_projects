from fastapi import FastAPI
from db import database
from endpoints import router


app = FastAPI()
app.include_router(router, prefix='/auth', tags=['users'])


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



