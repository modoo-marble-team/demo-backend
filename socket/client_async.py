import asyncio
import socketio

sio = socketio.AsyncClient(reconnection=True) 


@sio.event
async def connect():
    print("connected", sio.sid)
    await sio.emit("join", {"room": "lobby"})
    await sio.emit("chat", {"room": "lobby", "msg": "hello"})


@sio.event
async def server_ready(data):
    print("server_ready", data)


@sio.event
async def system(data):
    print("system", data)


@sio.event
async def chat(data):
    print("chat", data)


@sio.event
async def disconnect():
    print("disconnected")


async def main():
    await sio.connect("http://localhost:8000", auth={"nickname": "client1"})
    await sio.wait()


if __name__ == "__main__":
    asyncio.run(main())