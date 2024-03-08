#
# SETUP WEBSOCKETS
# 
from flask import request
from flask_socketio import join_room, send, emit

def setup_websockets(socket_io): 

    @socket_io.on("connect") 
    def connect(): 
        # get socket id 
        socket_id = request.sid 
        
        # output to console status of new connection
        print(f"> Received connection from socket_id [{socket_id}]")

    @socket_io.on("join_room")
    def on_join(data): 
        room_id = data
        sid = request.sid 
        
        print(f"> Received signal for [{sid}] to join room {room_id}")
        
        join_room(room_id)
        emit("joined_room", room_id)

        room_type = room_id.split(".")[0] 
        print("Room Type :", room_type)

        
        

