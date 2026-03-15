import asyncio
import websockets
import sys

# keep track of all connected clients so we can broadcast messages
connected_clients = set()

async def echo(websocket):
    # register client
    connected_clients.add(websocket)
    # send welcome message to new client
    await websocket.send("Welcome! You are connected to the WebSocket server.")
    try:
        async for message in websocket:
            # echo back to sender
            await websocket.send(message)
    except websockets.ConnectionClosed:
        pass
    finally:
        # unregister client
        connected_clients.remove(websocket)

async def broadcast_loop():
    """Read lines from stdin and broadcast them to all connected websockets."""
    # run in separate thread to avoid blocking event loop for sys.stdin
    loop = asyncio.get_running_loop()
    while True:
        # read line in thread
        line = await loop.run_in_executor(None, sys.stdin.readline)
        if not line:
            break
        message = line.rstrip("\n")
        if connected_clients:
            await asyncio.wait([client.send(message) for client in connected_clients])

async def main():
    # start websocket server and broadcast reader concurrently
    async with websockets.serve(echo, "0.0.0.0", 10000):
        await broadcast_loop()

if __name__ == "__main__":
    asyncio.run(main())

