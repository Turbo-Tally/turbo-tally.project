#
# :: ws_api.py 
# Create the WebSocket API of the backend.
#
import os 
from modules.core.logging import Logger
from flask_socketio import leave_room, join_room
from modules.main.common import Common

os.environ['EVENTLET_NO_GREENDNS'] = 'yes'

from flask_socketio import SocketIO 

def create_ws_api(app):
     
    # create socket_io app instance 
    socket_io = SocketIO(app, cors_allowed_origins="*") 

    Common.socket_io = socket_io

    @socket_io.on('connect')
    def on_connect(): 
        print("A client connected...")

    @socket_io.on('join')
    def on_join(data): 
        print("Joining " + data) 
        join_room(data)

    @socket_io.on('leave')
    def on_join(data): 
        print("Leave  " + data) 
        leave_room(data)

    @socket_io.on('forward') 
    def on_forward(data): 
        print('Forwarding ' + str(data)) 
        key = data['key']

        if key != os.getenv("APP_SECRET"): 
            return

        room = data['room'] 
        event = data['event'] 
        data = data['data'] 
        socket_io.emit(event, data, to=room)
    

    # return socket_io instance 
    return socket_io
