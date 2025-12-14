from fastapi_socketio import SocketManager
from fastapi import FastAPI

from app.utils.config import FRONTEND_ORIGINS

socket_manager: SocketManager | None = None # initialize socket manager

# intialize socket menager
def init_sockets(app: FastAPI):
    # define socket manager with app
    global socket_manager
    socket_manager = SocketManager(
        app=app,
        mount_location="/ws",
        cors_allowed_origins=FRONTEND_ORIGINS
    )
    
    @socket_manager.on("connect")
    async def on_connect(sid, environ):
        print(f"Client connected: {sid}")

    @socket_manager.on("disconnect")
    async def on_disconnect(sid):
        print(f"Client disconnected: {sid}")

    return socket_manager

# function that emits new events to connected clients
async def emit_new_event(data: dict):
    await socket_manager.emit("new-event", data)
