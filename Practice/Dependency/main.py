from fastapi import FastAPI, Header, Depends, Response
from fastapi.exceptions import HTTPException
from typing import Annotated


#! при дэпенденсях, когда наша функция видит много депенденсей, она идёт к самой первой - осуществляет её и даёт значение. Потом идёт ко второй с даденым
#! значением, осуществляет её, и так до последнего числа



def main_dep(x_token: Annotated[str, Header()]):
    if x_token == "token":
        return x_token
    raise HTTPException(status_code=400, detail="Token isn't right")


app = FastAPI(dependencies=[Depends(main_dep)])


def first_dependency(x_string: str):
    if x_string == "correct string":
        return x_string
    raise HTTPException(status_code=400, detail="not right x_string")


def second_dependency(x_integer: int):
    if x_integer % 2 != 0:
        raise HTTPException(status_code=400, detail="x_integer not even")
    return x_integer


def third_dependency(x_header: Annotated[str, Header()]):
    if x_header != "x":
        raise HTTPException(status_code=400, detail="x_header nor 'x'")
    return x_header



@app.get("/")
async def some_function(x_string = Depends(first_dependency), x_integer = Depends(second_dependency), x_header= Depends(third_dependency)):
    return {x_string:x_integer}




async def one():
    print("one")
    import random
    try:
        yield 4 + random.randint(1,10)
    finally:
        print('only first dependency has been ended')


async def two(number=Depends(one)):
    print("two")
    import random
    try:
        yield number + 67 + random.randint(-10, -5)
    finally:
        print('only second dependency has been ended')


async def three(number=Depends(two)):
    print("three")
    try:
        yield number + 52
    finally:
        print('only third dependency has been ended')


@app.get("/numbers")
async def numbers(number = Depends(three)):
    return number