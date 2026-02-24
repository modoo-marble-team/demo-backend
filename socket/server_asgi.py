import socketio

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = socketio.ASGIApp(sio)


@sio.event
async def connect(sid, environ, auth):
    nickname = (auth or {}).get("nickname") or sid[:6]
    await sio.save_session(sid, {"nickname": nickname})
    await sio.emit("server_ready", {"sid": sid, "nickname": nickname}, to=sid)


@sio.event
async def join(sid, data):
    room = (data or {}).get("room") or "lobby"
    await sio.enter_room(sid, room)

    session = await sio.get_session(sid)
    await sio.emit("system", {"msg": f'{session["nickname"]} joined {room}'}, room=room)


@sio.event
async def leave(sid, data):
    room = (data or {}).get("room") or "lobby"
    await sio.leave_room(sid, room)

    session = await sio.get_session(sid)
    await sio.emit("system", {"msg": f'{session["nickname"]} left {room}'}, room=room)


@sio.event
async def chat(sid, data):
    room = (data or {}).get("room") or "lobby"
    msg = str((data or {}).get("msg") or "")

    session = await sio.get_session(sid)
    payload = {"room": room, "nickname": session["nickname"], "msg": msg}
    await sio.emit("chat", payload, room=room)


@sio.event
async def disconnect(sid):
    pass