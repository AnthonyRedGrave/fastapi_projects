from fastapi import FastAPI
from api.auth import router


app = FastAPI()

app.include_router(router)


# Главная страница
# Поиск по городам, 
# отображение карты, 
# прогноз погоды на неделю, 
# подключение подписки, чтобы смотреть изменения в городе
# csv import-export данных о погоде в городе


@app.get('/')
async def main():
    return {'1':'2'}



