#
# :: ws_api.py 
# Create the WebSocket API of the backend.
#
import os 
os.environ['EVENTLET_NO_GREENDNS'] = 'yes'

from flask_socketio import SocketIO 

def create_ws_api(app): 
    # create socket_io app instance 
    socket_io = SocketIO(app) 

    # return socket_io instance 
    return socket_io
