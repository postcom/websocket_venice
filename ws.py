from fastapi import FastAPI
from fastapi.websockets import WebSocket

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "WebSocket server is running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Welcome! You are connected to the WebSocket server.")
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(data)
    except:
        pass

