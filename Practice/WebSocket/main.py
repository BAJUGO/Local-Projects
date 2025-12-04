from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form onsubmit="sendMessage(event)">
            <input type="text" id="messageInput" autocomplete="off">
            <button type="submit">Send</button>
        </form>
        
        <ul id="messagesList">
        </ul>
        
        <script>
        var ws = new WebSocket("ws://localhost:8000/ws")
        
        ws.onmessage = function(event) {
        var messagesList = document.getElementById("messagesList")
        var message = document.createElement("li")
        message.textContent = event.data
        messagesList.appendChild(message) };
        
        function sendMessage(event) {
        var input = document.getElementById("messageInput")
        ws.send(input.value)
        input.value = ''
        
        event.preventDefault()
        };
        
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


list_of_illegal = ["fuck", "KYS", "fucking", "bitch", "shit"]

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()     # Принимаем websocket соединение. Только после этого можно обмениваться сообщениями при помощи receive и send text
    while True:   # Бесконечный цикл. Пока клиент не закроет подключение, будет эта ерунда выполняться
        data = await websocket.receive_text()
        new_words = []
        for word in data.split():
            if word in list_of_illegal:
                word = "*" * len(word)
            new_words.append(word)
        new_data = " ".join(new_words)
        await websocket.send_text(new_data)