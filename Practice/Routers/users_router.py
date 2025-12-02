from fastapi import APIRouter, Depends, Header, Body
from typing import Annotated
from fastapi.exceptions import HTTPException
from .routered_router import router as additional_router


def user_dep(user_token: Annotated[str, Header()]):
    if user_token != "user":
        raise HTTPException(status_code=400, detail="You can't do it!")




router = APIRouter(
    dependencies=[Depends(user_dep)],
    prefix="/users",
    tags=["Users"]
)

router.include_router(additional_router)

@router.get("/")
async def read_users():
    return {"There are some ": "users!"}



@router.post("/")
async def post_something(the_thing_you_are_posting: Annotated[str, Body()]):
    return the_thing_you_are_posting

