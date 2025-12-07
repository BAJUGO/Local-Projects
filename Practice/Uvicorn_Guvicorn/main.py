from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def return_smth():
    return {"Hello": "user"}


#* При двух воркерах
#! uvicorn "Practice.Uvicorn_Guvicorn.main:app" --host 0.0.0.0 --port 5291 --workers 2
#! INFO:     Uvicorn running on http://0.0.0.0:5291 (Press CTRL+C to quit)
#! INFO:     Started parent process [2864]                                              Запускаем главный процес Uvicorn, который ничего не обрабатывает, но следит за всеми воркерами
#! INFO:     Started server process [14140]                                             Запускаем воркера
#! INFO:     Waiting for application startup.                                           Делаем Lifespane startup
#! INFO:     Application startup complete.                                              Сделал все Lifespane startup события
#! INFO:     Started server process [6812]                                              И так для другого воркера
#! INFO:     Waiting for application startup.
#! INFO:     Application startup complete.
#!
#! Роутеры работают от свободы - если 1 занят одним запросом - выручает другой. Это при def, при async (и тех условиях, обговоренных в StreamingResponse) 1 воркер может хоть 20 заказов брать






#* По непонятным мне и скорее всего Богу причинам, у меня работает только такой вариант работы с несколькими воркерами
#! uvicorn "Practice.Uvicorn_Guvicorn.main:app" --host 0.0.0.0 --port 5291 --workers 2