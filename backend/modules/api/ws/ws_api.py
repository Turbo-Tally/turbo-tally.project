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
        pass 

    @socket_io.on('join')
    def on_join(data): 
        print("Joining " + data) 
        join_room(data)

    @socket_io.on('leave')
    def on_join(data): 
        print("Leave  " + data) 
        leave_room(data)
    

    # return socket_io instance 
    return socket_io
