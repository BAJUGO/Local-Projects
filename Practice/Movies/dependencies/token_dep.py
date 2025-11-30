from fastapi import Header
from ..custom_exceptions import custom_exc


def check_admin_token(admin_token = Header()):
    if admin_token != "admin":
        raise custom_exc.not_enough_rights()


def check_ultra_admin_token(ultra_admin_token = Header()):
    if ultra_admin_token != "ultra-admin":
        raise custom_exc.not_enough_rights()