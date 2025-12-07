from fastapi import FastAPI
from fastapi.exceptions import HTTPException
import requests

app = FastAPI()

@app.get("/hello")
def hello(name: str = "world"):
    if name.isdigit():
        raise HTTPException(status_code=400, detail="You can't do int")
    return {"message": f"Hello {name}"}



@app.get("/jokes")
def joke():
    r = requests.get("https://api.chucknorris.io/jokes/random")
    data = r.json()
    return {"joke": data['value']}

