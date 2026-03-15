import asyncio
import websockets
import os

def process_request(path, headers):
    """Handle HTTP requests for health checks."""
    if path == '/':
        return (200, [], b'WebSocket server is running\n')
    return None  # Proceed with WebSocket handshake

async def echo(websocket):
    await websocket.send("Welcome! You are connected to the WebSocket server.")
    try:
        async for message in websocket:
            await websocket.send(message)
    except websockets.ConnectionClosed:
        pass

async def main():
    port = int(os.environ.get('PORT', 8765))
    async with websockets.serve(echo, "0.0.0.0", port, process_request=process_request):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())

