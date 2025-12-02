from fastapi import Request, BackgroundTasks, Response
from datetime import datetime

def fake_log(data_to_write):
    #with open("file.txt", "a") as file:
        #file.write(data_to_write)
        pass


#! ИНТЕРЕСНАЯ ДЕТАЛЬ: ПРИ ДВУХ MIDDLEWARE, ПОРЯДОК СЛЕДУЮЩИЙ - РЕКВЕСТНОЕ ДЕЙСТВИЕ А, РЕКВЕСТНОЕ ДЕЙТСВИЕ Б
#! РЕСПОНСНОЕ ДЕЙСТВИЕ Б, РЕСПОНСНОЕ ДЕЙСТВИЕ А.
#! То есть сначала мы напечатали бы в наш файл user_agent и time, а только потом path, ip и time


async def log_middleware_a(request: Request, call_next):
    path = str(request.url.path)
    ip = str(request.client.host)
    time = datetime.now()

    data_to_write = (f"path - {path}\n"
                     f"ip - {ip}\n"
                     f"time - {time}\n\n\n")

    response = await call_next(request)

    if response.background:
        response.background.tasks.append(fake_log, data_to_write)
    else:
        bgt = BackgroundTasks()
        bgt.add_task(fake_log, data_to_write)
        response.background = bgt

    response.headers.update({"header": "middleware_A"})
    return response



async def log_middleware_b(request: Request, call_next):
    user_agent = str(request.headers.get("user_agent"))
    time = datetime.now()

    data_to_write = (f"user_agent - {user_agent}\n"
                     f"time - {time}\n\n\n")

    response = await call_next(request)

    if response.background:
        response.background.tasks.append(fake_log, data_to_write)
    else:
        bgt = BackgroundTasks()
        bgt.add_task(fake_log, data_to_write)
        response.background = bgt
    response.headers.update({"something":"cool"})
    return response