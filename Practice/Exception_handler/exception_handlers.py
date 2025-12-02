from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from .custom_exceptions import SixSevenException, JustAWrongNumberException
from fastapi.responses import JSONResponse

#! немного теории - когда в api происходит исключение, мы ищем кастомные хэндлеры. Затем если их нет - идём в кастомные
#! Если и они сломались, то Internal Error 500
#! В любой response можно передавать headers, background, status_code и всё такое. Всё будет воркать отлично
#! В обычный HTTPException (и в целом без ответа) я никак не передам BackgroundTask
#! Логировать ошибки нужно через BackgroundTasks:
#!
#!function(*args, **kwargs):
#!  with open(file.txt, "a") as file:
#!      file.write()
#!
#! app.exception_handler()...
#!...
#! bc = BackgroundTasks()
#! bc.add_task(function, *args, **kwargs)
#! return Response(background=bc)
#! Даже HTTPException можно сделать так, чтобы она возвращала JSONResponse, что позволит добавить bgt




def exception_handler_a(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def rve_handler(request: Request, exc: RequestValidationError):
        print(f"Пользователь ввёл не валидные данные!\n"
              f"{request.body}\n"
              f"{exc.errors}\n\n")
        return await request_validation_exception_handler(request=request, exc=exc)


    @app.exception_handler(HTTPException)
    async def http_handler(request: Request, exc: HTTPException):
        print(f"status code - {exc.status_code}\n"
              f"request.body - {request.body}\n"
              f"http_exc detail - {exc.detail}\n\n\n")
        return await http_exception_handler(request, exc)


    @app.exception_handler(SixSevenException)
    async def six_seven_handler(request: Request, exc: SixSevenException):
        print(f"exc.name - {exc.name}\n"
              f"exc.detail = {exc.detail}\n"
              f"time of occur = {exc.time_of_occur}\n"
              f"user-agent - {request.headers.get("user_agent")}")
        return JSONResponse(status_code=467, content={"six seven": 67, 67: "six_seven"})


    @app.exception_handler(JustAWrongNumberException)
    async def jwne_handler(request: Request, exc: JustAWrongNumberException):
        your_lucky_time = exc.random_number
        print(f"exc something - {exc.reason}\n"
              f"exc.more_something - your_lucky_time")
        if your_lucky_time >= 6:
            return JSONResponse(status_code=200, content={"You are lucky this time! You may go!": "Bla bla bla"})
        else:
            return JSONResponse(status_code=400, content={"Unlucky... So, better luck next time?)": "Bla bla bla 2"}, headers={"Dont":"Worry"})
