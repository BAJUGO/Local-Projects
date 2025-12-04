from typing import Annotated

from fastapi import (
    Cookie,
    Depends,
    FastAPI,
    Query,
    WebSocket,
    WebSocketException,
    status, # Это можно использовать как для HTTP, так и для WebSocket
)
from fastapi.responses import HTMLResponse

app = FastAPI()


#! По поводу form[label, value] - label просто делает так скажем подпись для этого поля. У нас после label сразу идёт itemId и Token, в которых
#! тот самый <input type="text"..., который был в предыдущем примере
#! По поводу ; - ставь их после объявления переменных, и объявления безымянных функций. В остальных случаях не нужно. Безымянные функции на примере onmessage - там
#! просто осуществляется какая-то функция

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form onsubmit="sendMessage(event)">
            <label>Item ID <input type="text" id="inputID" value="Foo" autocomplete="off"></label>
            <label>Token <input type="text" id="inputToken" value="token" autocomplete="off"></label>
            <button onclick="connect(event)">Connect</button>
            <hr>
            <br>
            <label>Text <input type="text" id="inputText" autocomplete="off"></label>
            <button type="submit">Send</button>
        </form>
        
        <ul id="messagesList">
        </ul>
        
        <script>
        
        var ws = null;
        
        function connect(event) {
        var ID = document.getElementById("inputID");
        var token = document.getElementById("inputToken");
        ws = new WebSocket("ws://localhost:8000/items/" + ID.value + "/ws?token=" + token.value)
        
        ws.onmessage = function(event) {
            var messagesList = document.getElementById("messagesList")
            var message = document.createElement("li")        
            message.textContent = event.data
            messagesList.appendChild(message)
        };
        
        event.preventDefault()
        }
        
        function sendMessage(event) {
        var input = document.getElementById("inputText")
        ws.send(input.value)
        input.value = ''
        event.preventDefault()
        }
        
        
        
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


async def get_cookie_or_token(
    websocket: WebSocket,
    session: Annotated[str | None, Cookie()] = None,
    token: Annotated[str | None, Query()] = None,
):
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


@app.websocket("/items/{item_id}/ws")
async def websocket_endpoint(
    *,
    websocket: WebSocket,
    item_id: str,
    q: int | None = None,
    cookie_or_token: Annotated[str, Depends(get_cookie_or_token)],
):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(
            f"Session cookie or query token value is: {cookie_or_token}"
        )
        if q is not None:
            await websocket.send_text(f"Query parameter q is: {q}")
        await websocket.send_text(f"Message text was: {data}, for item ID: {item_id}")