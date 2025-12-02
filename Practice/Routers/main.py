from .users_router import router as users_router
from .items_router import router as items_router
from fastapi import FastAPI, Depends, Header
from typing import Annotated
from fastapi.exceptions import HTTPException


def additional_dep(x_string: str):
    if x_string != "iks string":
        raise HTTPException(status_code=400, detail="No detail")
    return x_string


def main_dep(main_token: Annotated[str, Header()]):
    if main_token != "main_token":
        raise HTTPException(status_code=400, detail="You are 400")




app = FastAPI(
    dependencies=[Depends(main_dep)]
)



app.include_router(users_router)
app.include_router(items_router)


@app.get("/something")
async def return_something(x_string = Depends(additional_dep)):
    return "something"