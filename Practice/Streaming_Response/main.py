from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse
import time
import asyncio
from pathlib import Path as pl_path

app = FastAPI()


# async def wait_time():
#     for i in range(5):
#         yield f"Chunk {i}"
#         time.sleep(2)
#
#
# @app.get("/")
# async def stream():
#     return StreamingResponse(wait_time(), media_type="text/plain")
#
#
#
# async def generator():
#     x = 0
#     for i in range(5):
#         yield f"{x}"
#         x += 1
#         await asyncio.sleep(2)
#
# @app.get("/itter")
# async def get_itter():
#         return StreamingResponse(generator(), media_type = "text/plain")




async def file_reader(file_path, chunk_size = 1024):
    with open(file_path, "rb") as f:               #* rb означает открытие файла в бинарном режиме
        while chunk := f.read(chunk_size):         #* При помощи этого моржа мы присваиваем chunk какие-то байты. Пока они есть - это True, следовательно while True выполняется.
            yield chunk
            await asyncio.sleep(0.5)


@app.get("/cachy_os")
async def read_pycharm():
    file_path = pl_path("D:/Frequent proggrams/cachyos-desktop-linux-250713.iso")
    headers = {"Content-Length": str(file_path.stat().st_size)}
    return StreamingResponse(file_reader(file_path), media_type="application/zip", headers=headers)




#! Сервер сам читает файл, и только потом отдаёт. В варианте сверху во время загрузки не видно, сколько осталось до скачивания файла, ибо сам сервер этого не знает
#! В варианте ниже же сервер сначала читает файл целиком, и только потом позволяет его скачивать. Это связано с заголовком content-length, который bad отдаёт в ответе
#! В примере выше, при помощи библиотеки pathlib мы всё таки передали размер файла в header Content-Length, так что сколько осталось скачивать мы видим.
#! Немного про pathlib - там есть много интересных методов, по типу file_path.exists(), file_path.is_dit() и другие. stat() просто имеет интересную статистику, по типу размера st_size
#! + ещё st_mtime - время последнего изменения


@app.get("/cachy_os_bad")
async def read_pycharm():
    file_path = "D:/Frequent proggrams/cachyos-desktop-linux-250713.iso"
    return FileResponse(file_path, media_type="application/zip")





#! Ещё пару банальных примеров, которые 1 в 1 схожи с прочими





async def real_file_reader(path, chunk_size=1024):
    with open (path, "rb") as f:
        while chunk := f.read(chunk_size):
            yield chunk
            await asyncio.sleep(0.1)


@app.get("/read_file")
async def read_file_in_stream():
    path = pl_path("D:/pycharm-2025.2.4.exe")
    headers = {"Content-Length": str(path.stat().st_size)}
    return StreamingResponse(real_file_reader(path), headers=headers)



from io import StringIO
import csv


async def csv_gen():
    header = ['id', 'name', 'email']
    yield ",".join(header) + "\n"

    for i in range(10000):
        row = [str(i), f"user{i}", f"email{i}@example.com"]
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(row)
        yield output.getvalue()


@app.get("/download-csv")
async def download_csv():
    return StreamingResponse(csv_gen(), media_type="text/csv")




async def read_many_files(files):
    for file in files:
        with open(file, "rb") as f:
            while chunk := f.read(1024):
                yield chunk
                await asyncio.sleep(0.01)


@app.get("/download_many_files")
async def many_files():
    files = ["D:/pycharm-2025.2.4.exe", "D:/chlen/chlen.rar"]

    headers = {"Content-Length": str(sum(pl_path(x).stat().st_size for x in files))} # Интересный способ записать ЭТО -
    # suma = 0
    # for file in files:
    #     file = pl_path(file).stat().st_size
    #     suma += file
    #
    # headers = {"Content-Length": str(sum)}
    return StreamingResponse(read_many_files(files), media_type="application/zip", headers=headers)



from datetime import datetime

async def generate_time():
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        yield f"Time now is {now}\n"
        await asyncio.sleep(1)


@app.get("/time")
async def to_know_the_time():
    return StreamingResponse(generate_time(), media_type="text/event-stream")
                                                        #! Event-stream, в отличии от plain кидает не просто текст, а отдельные event, как при websocket
                                                        #! Позволяя обрабатывать каждое событие. В противном случае мы просто получаем текст, и добавляем его на страницу






@app.get("/end1")
async def sdad():
    print(1)
    time.sleep(3)
    print(2)

@app.get("/end2")
async def sdsad2():
    print(3)
    await asyncio.sleep(3)
    print(4)

@app.get("/end3")
def sdasd3():
    print(5)
    time.sleep(5)
    print(6)



#! Объяснение этой непонятной фигни: Uvicorn использует несколько воркеров (потоков), когда происходит новое обращение, а функция написана через def.
#! Он видит time.sleep(5), и блокирует ОДИН ИЗ ВОЗМОЖНЫХ потоков. Поэтому они выполняются будто бы асинхронно.
#!
#! Пример выше: при async мы работаем с одним потоком, а await говорит: "Я на 3 секунды отдохну, но ты можешь обработать и другие запросы в моём потоке"
#!
#! Ещё один пример выше: async НЕ создаёт новый поток. А что делает time sleep? Блокирует поток. Никакой параллели нету