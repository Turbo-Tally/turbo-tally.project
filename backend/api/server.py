
from flask import Flask


class APIServer: 
    def __init__(self): 
        from api.controllers.HttpController import HttpController
        from api.controllers.WsController import WsController 
    
        self.app = Flask(__name__)

        self.HttpController = HttpController
        self.WsController = WsController

        self.makeRoutes() 

    def makeRoutes(self):
        
        # GET /ping
        self.app.add_url_rule(
            "/ping", 
            view_func=self.HttpController.ping
        )

        # GET /analyze 
        self.app.add_url_rule(
            "/analyze", 
            view_func=self.HttpController.analyze
        )

    def start(self): 
        print("@ Running on localhost:80")
        self.app.run("0.0.0.0", 80)

server = APIServer() 
server.start() 