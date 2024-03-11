from flask import request 
from flask_socketio import emit, send, join_room, leave_room

def make_ws_api(socket_io):

    @socket_io.on("connect")
    def on_connect(): 
        print(f"> Client connected    -> SID: [{request.sid}].")


    @socket_io.on("disconnect")
    def on_disconnect():
        print(f"> Client disconnected -> SID: [{request.sid}].")