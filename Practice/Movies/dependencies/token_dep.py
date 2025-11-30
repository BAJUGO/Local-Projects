from fastapi import Header
from ..custom_exceptions import custom_exc


def check_admin_token(admin_token = Header()):
    if admin_token != "admin":
        raise custom_exc.not_enough_rights()


