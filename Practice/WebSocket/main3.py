from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json

'''Tips'''
#* Ловим WebSocketDisconnect при отправке сообщений, чтобы сервер не падал, если клиент отключился
#* Никогда не забываем вызывать await websocket.accept() перед receive/send, иначе WebSocket не подключен
#* Проверяем payload на JSONDecodeError, чтобы принимать как простые строки или как объекты с target
#* Всегда проверяем, что target существует в active_connections перед отправкой приватного сообщения


app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket's chat</h1>
        <h2>Your client-ID is <span id="client_id"></span></h2>
        <form onsubmit="sendMessage(event)">
            <label><p>Write there your input</p><input type="text" id="inputText" autocomplete="off"></label>
            <br>
            <button type="submit">Send</button>
            <button onclick="sendMessageDirect(event)">Send Directly</button>
            <br>
            <label><p>Someone's ID for direct message</p><input type="text" id="inputTextDirect" autocomplete="on"></label>
        </form>
        
        <ul id="messagesList">
        </ul>
        
        <script>
        var clientID = Date.now();
        document.querySelector("#client_id").textContent = clientID
        var websocket = new WebSocket(`ws://localhost:8000/websocket/${clientID}`);
            
        websocket.onmessage = function(event) {
            var messages = document.getElementById("messagesList")
            var message = document.createElement("li")
            message.textContent = event.data
            messages.appendChild(message)
        };
        
        function sendMessage(event) {
            var input = document.getElementById("inputText")
            websocket.send(input.value)
            input.value = ''
            event.preventDefault()
        };
        
        function sendMessageDirect(event) {
            var input = document.getElementById("inputText")
            var target_id = document.getElementById("inputTextDirect")
            var message = JSON.stringify({text : input.value, target: target_id.value})
            websocket.send(message)
            input.value = ''
            target_id.value = ''
            event.preventDefault()
        };
            
            
        </script>
    </body>
</html>
"""


@app.get("/")
async def main():
    return HTMLResponse(html)




#! ФУНКЦИИ ДЛЯ ВЕБСОКЕТА И ЕГО КЛАССА
async def direct_message_to_you_function(websockets: dict, ws: WebSocket,websocket: WebSocket, message: str):
    try:
        await ws.send_text(f"Client {websockets[websocket]} send a direct message to you: {message}")
    except WebSocketDisconnect:
        await ws_manager.disconnect(ws)

async def direct_message_from_you_function(websocket: WebSocket, target: int):
    try:
        await websocket.send_text(f"Your message to {target} has been send")
    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket)

async def check_target_function(target_raw, websocket, message):
    if target_raw is None or str(target_raw).strip() == "" or not target_raw.isdigit():
        await ws_manager.broadcast(websocket, message)
    else:
        target = int(target_raw)
        await ws_manager.direct_response(websocket, message, target)


async def broadcast_without_you_function(connection: WebSocket, websockets: dict, message: str, websocket: WebSocket):
    try:
        await connection.send_text(f"Client {websockets[websocket]} said: {message}")
    except WebSocketDisconnect:
        await ws_manager.disconnect(connection)


#! КЛАСС CONNECTION MANAGER
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[WebSocket, int] = {}


    async def connect(self, websocket: WebSocket, client_id):
        await websocket.accept()
        self.active_connections[websocket] = client_id
        for connection in self.active_connections.keys():
            if connection != websocket:
                await connection.send_text(f"New client connected: {client_id}")
        await websocket.send_text(f"You have joined the chat!")


    async def disconnect(self, websocket: WebSocket):
        id_of_deleted = self.active_connections[websocket]
        self.active_connections.pop(websocket)
        for connection in self.active_connections.keys():
            try:
                await connection.send_text(f"User has been disconnected. Their ID was {id_of_deleted}")
            except WebSocketDisconnect:
                self.active_connections.pop(connection)


    async def broadcast(self, websocket: WebSocket, message: str):
        for connection in self.active_connections.keys():
            if connection != websocket:
                await broadcast_without_you_function(connection, self.active_connections, message, websocket)
        try:
            await websocket.send_text(f"You said: {message}")
        except WebSocketDisconnect:
            await self.disconnect(websocket)


    async def direct_response(self, websocket: WebSocket, message: str, target: int):
        found = False
        for ws, ids in self.active_connections.items():
            if ids == target:
                found = True
                await direct_message_to_you_function(self.active_connections, ws, websocket, message)
        if found:
            await direct_message_from_you_function(websocket, target)
        else:
            await websocket.send_text(f"There was no such ID - {target}")




ws_manager = ConnectionManager()




#! ВЕБ СОКЕТ
@app.websocket("/websocket/{client_id}")
async def work_with_websocket(client_id: int, websocket: WebSocket):
    await ws_manager.connect(websocket, client_id)
    while True:
        try:
            data = await websocket.receive_text()

            try:
                payload = json.loads(data)
                message = payload.get("text")
                target_raw = payload.get("target")
                await check_target_function(target_raw, websocket, message)

            except json.JSONDecodeError:
                await ws_manager.broadcast(websocket, data)

        except WebSocketDisconnect:
            await ws_manager.disconnect(websocket)
            break













