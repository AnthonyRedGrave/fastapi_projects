from fastapi import FastAPI
# from worker import create_task


app = FastAPI()


# Главная страница
# Поиск по городам, 
# отображение карты, 
# прогноз погоды на неделю, 
# подключение подписки, чтобы смотреть изменения в городе


@app.get('/')
async def main():
    # create_task(1)
    return {'1':'2'}



