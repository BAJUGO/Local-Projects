from fastapi import Request, BackgroundTasks
import uuid

def log_data(data):
    with open("D:\LocalProjects\Practice\Movies\log.txt", "a") as file:
        file.write(data)


async def log(request: Request, call_next):
    method = str(request.method)
    path = str(request.url.path)
    query = str(request.url.query)
    user_agent = str(request.headers.get("User-Agent"))

    request_id = str(uuid.uuid4())

    response = await call_next(request)

    data = (f"method - {method}\n"
            f"path - {path}\n"
            f"querys - {query}\n"
            f"user_agent - {user_agent}\n"
            f"request_id - {request_id}\n\n")
    bc = BackgroundTasks()
    bc.add_task(log_data, data)

    if response.background:
        response.background.tasks.append(bc)
    else:
        response.background = bc

    response.headers["request_id"] = request_id

    return response