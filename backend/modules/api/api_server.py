#
# :: api_server.py 
# Set up API Server (REST + WS API)
# 
from modules.core.logging import Logger

class APIServer: 
    def __init__(self):
        Logger.log("api/api_server", "> Hello, from API Server!")

        self.flask_app = None 
        self.socket_io = None 
        
    def init(self):
        Logger.log("api/api_server", "> Initializing API Server...") 
        
        # create flask app 
        Logger.log("api/api_server", "> Initializing Flask app...")
        from .rest_api import create_rest_api
        self.flask_app = create_rest_api() 

        # create websocket app 
        Logger.log("api/api_server", "> Initializing Flask-SocketIO app...")
        from .ws_api import create_ws_api 
        self.socket_io = create_ws_api(self.flask_app)

    def run(self):
        Logger.log("api/api_server", "> Running API Server...")
        self.socket_io.run(
            self.flask_app, 
            "0.0.0.0", 80,
            debug=True,
            allow_unsafe_werkzeug=True    
        )