from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from .exception_handlers import exception_handler_a
from .custom_exceptions import SixSevenException, JustAWrongNumberException

app = FastAPI()

exception_handler_a(app)


@app.get("/cool/{n}")
async def something(n: int):
    if n == 14:
        raise HTTPException(status_code=400, detail="Watafak is going out here?")
    if n == 67:
        raise SixSevenException(detail="six seven exception!")
    if n == 777:
        raise JustAWrongNumberException(reason="you typed 777 at the path )")
    return n