from flask import Flask, send_file, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from time import sleep
from threading import Thread
import socket
import os 
import subprocess

from core.dbal import DBAL 
from core.cache import Cache 

Cache.init()
DBAL.init()

app = Flask(
    __name__,
    static_url_path='', 
    static_folder='../static'
)

socketio = SocketIO(app, cors_allowed_origins='*')

# HTTP REQUESTS
def setup_rest():
    @app.route("/ping")
    def ping():
        return "PONG" 


    @app.route("/mock-client")
    def mock_client():
        return send_file("../mock-client.html")

    @app.route("/analyze")
    def analyze(): 
        from backend.core.analyzer import Analyzer
        stream_ids = request.args.get("streams").split(',') or []
        task_id = Analyzer.process_request(stream_ids)         


# WEBSOCKET REQUESTS 
def setup_websockets():

    @socketio.on("connect") 
    def connect(auth): 
        sid = request.sid
        print(f"@ Client [{sid}] has connected.")

    @socketio.on("join") 
    def join(data): 
        pass 



if __name__ == "__main__": 
    # setup API server
    setup_websockets() 
    setup_rest() 

    # output information about where the server is running on
    private_ip = subprocess.getoutput("hostname -I").strip()
    print(f"@ Running `scans.backend` on [{private_ip}:80]...")
    socketio.run(app, "0.0.0.0", 80) 
