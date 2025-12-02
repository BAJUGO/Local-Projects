from fastapi import APIRouter, Depends, Header, Body
from typing import Annotated
from fastapi.exceptions import HTTPException


def items_dep(items_token: Annotated[str, Header()]):
    if items_token != "token":
        raise HTTPException(status_code=404, detail="Not right token!")



router = APIRouter(
    prefix="/items",
    dependencies=[Depends(items_dep)],
    tags=["Items"]
)


@router.get("/")
async def return_items():
    return {"there are": "items!"}


@router.post("/")
async def reeeturn_items(something: Annotated[list, Body()]):
    return something