from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI

def fake_ml_model(x: int):
    return x * 2

ml_models = {}



#! Так как у меня стоит uvicorn --reload, то при сохранении изменения выполняется и часть ДО, и часть ПОСЛЕ
@asynccontextmanager
async def lifespan(app : FastAPI):

    ml_models["smart_model"] = fake_ml_model
    with open("Practice/Lifespan/new.txt", "a") as file:
        file.write(f"ДО РАБОТЫ ПРИЛОЖЕНИЯ {datetime.now()}\n")
    #! Всё что выше - выполнится ДО запуска приложения
    yield
    with open("Practice/Lifespan/new.txt", "a") as file:
        file.write(f"ПОСЛЕ РАБОТЫ ПРИЛОЖЕНИЯ {datetime.now()}\n\n\n\n")

    #! Всё что ниже - выполнится ПОСЛЕ прекращения работы приложения
    ml_models.clear()



app = FastAPI(lifespan=lifespan)


@app.get("/predict")
async def predict_smth(x: float):
    result = ml_models["smart_model"](x)
    #! интересный вариант - в лист мы поместили не саму функцию, а объект-функцию. И здесь мы вызываем её из списка, и сразу в скобочках передаём аргумент
    return {"Result": result}
