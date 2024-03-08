from flask import Flask 
from flask_socketio import SocketIO
import subprocess
from dotenv import load_dotenv 
from scans.data.DataWrapper import DataWrapper

load_dotenv(".env")

# initialize data wrappers 
DataWrapper.register("tasks", "task_id") 
DataWrapper.register("messages", "message_id") 
DataWrapper.register("exchange_rates", "date") 
DataWrapper.register("streams", "stream_id")

# create Flask application 
app = Flask(
    __name__, 
    static_url_path='', 
    static_folder='static/'
)
app.config['SECRET_KEY'] = "1234" 

# create SocketIO application
socket_io = SocketIO(app) 

# create routes 
from setup_routes import setup_routes 
setup_routes(app)

# create websocket handler 
from setup_websockets import setup_websockets
setup_websockets(socket_io)

# run socket io application 
ip_address = str(subprocess.getoutput("hostname -I")).strip()
print(f"API Server: Running in [{ip_address}]...")
socket_io.run(app, "0.0.0.0", 80, debug=True)
