from flask import Flask 
from flask_socketio import SocketIO
from dotenv import load_dotenv 
import os

load_dotenv(".env")

# create flask app
app = Flask(
    __name__, 
    static_url_path="",
    static_folder="./static",
    template_folder=os.path.abspath("./templates")
)

# setup data models 
import data.setup_data_models

# create socket.io app 
socket_io = SocketIO(app) 

# setup REST routes 
from .rest.api import make_rest_api 
make_rest_api(app) 

# setup REST routes
from .ws.api import make_ws_api 
make_ws_api(socket_io)

# set up task manager 
from scans.TaskManager import task_manager
task_manager.socket_io = socket_io 
task_manager.flask_app = app

# run server
socket_io.run(app, "0.0.0.0", 80, debug=True)