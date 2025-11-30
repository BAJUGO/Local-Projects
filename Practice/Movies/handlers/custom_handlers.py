from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.exception_handlers import http_exception_handler
from datetime import datetime


def find_p_m_i(request: Request, additional = None):
    return (f"path - {str(request.url.path)}\n"
            f"method - {str(request.method)}\n"
            f"IP - {str(request.client.host)}\n"
            f"time - {datetime.now()}\n"
            f"additional (if is) - {additional}\n\n\n")



def log_exception(data):
    with open("D:\LocalProjects\Practice\Movies\exceptions_log.txt", "a") as file:
        file.write(data)



def create_exceptions_handlers(app: FastAPI):

    @app.exception_handler(HTTPException)
    async def work_with_http_exc(request: Request, exc: HTTPException):
        info = find_p_m_i(request, additional = [exc.detail, exc.status_code])
        try:
            return await http_exception_handler(request, exc)
        finally:
            log_exception(info)




