from fastapi import APIRouter, Depends, Body
from ..dependencies.token_dep import check_ultra_admin_token
from ..ultra_services.create_new_table import create_class, create_table
from typing import Annotated, Any
from sqlalchemy import Column, Integer, String


router = APIRouter(dependencies=[Depends(check_ultra_admin_token)])


@router.post("/create_table")
async def create_new_db_object(class_name: str, table_name: str, columns: dict[str, Any] = Body()
):
    new_class = create_class(class_name, table_name, **columns)
    create_table(new_class)
    return {"status": "table_created", "class_name" : class_name}

