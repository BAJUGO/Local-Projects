from typing import Annotated
from fastapi import FastAPI, WebSocket, Cookie, Query, Depends, WebSocketException, status
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat with Cookie and Query</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="connect(event)">
            <label>Item ID: <input type="text" id="itemId" autocomplete="off" value="foo"/></label>
            <label>Token: <input type="text" id="token" autocomplete="off" value="some-key-token"/></label>
            <button>Connect</button>
            <hr>
            <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = null;
            function connect(event) {
                var itemId = document.getElementById("itemId").value;
                var token = document.getElementById("token").value;
                ws = new WebSocket("ws://localhost:8000/items/" + itemId + "/ws?token=" + token);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                event.preventDefault()
            }
            function sendMessage(event) {
                var input = document.getElementById("messageText")
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
    websocket: WebSocket,
    item_id: str,
    cookie_or_token: Annotated[str, Depends(get_cookie_or_token)],
    q: int | None = None,

):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Session cookie or query token value is: {cookie_or_token}")
        if q is not None:
            await websocket.send_text(f"Query parameter q is: {q}")
        await websocket.send_text(f"Message text was: {data}, for item ID: {item_id}")