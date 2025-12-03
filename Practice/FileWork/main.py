from fastapi import FastAPI, UploadFile, Request
from fastapi.responses import FileResponse, JSONResponse



app = FastAPI()


#! middleware НЕ МОЖЕТ выбросить любую exception до того, как будет создан response. Сначала нужно создать респонс, а потом все
#! Хэндлеры будут работать. Это важно запомнить. Также про content-length - он включает только body(), тело запроса. Не включает path, query и т.д
#! if content_length and int... проверка на то, существует ли в целом content_length, а потом проверка его размера


max_size = 2 * 1024 * 1024  # 2 МБ

@app.middleware("http")
async def work_with_file_size(request: Request, call_next):
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > max_size:
        return JSONResponse(status_code=403, content={"Pizdariki?": "Pizdariki."})
    return await call_next(request)




@app.post("/files/request_file")
async def files(file: UploadFile):
    return f'''filename - {file.filename}  ------------  file type - {file.content_type}      ------------     file headers? - {file.headers}    ------------   file size - {file.size}'''



@app.post("/a_lot_of_files")
async def return_lots_of_files(list_of_files: list[UploadFile]):
    return [x.filename for x in list_of_files]



@app.get("/files/get_presentation")
async def return_file():
    return FileResponse("D:/chlen/chle1n.rar",filename="virus.rar", media_type="application/octet-stream")



