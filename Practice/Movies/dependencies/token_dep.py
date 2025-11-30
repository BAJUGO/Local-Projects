from fastapi import Header
from fastapi.exceptions import HTTPException


def check_admin_token(admin_token = Header()):
    if admin_token != "admin":
        raise HTTPException(status_code=409, detail="You are not good enough")


