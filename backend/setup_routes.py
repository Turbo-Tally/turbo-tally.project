#
# SETUP ROUTES 
#
from flask import send_file, request
import uuid
from scans.core.TaskManager import TaskManager
from threading import Thread
import os

def setup_routes(app): 

    #
    # GET /
    #  
    @app.route("/")
    def index(): 
        return """
            <div 
                style="
                    display: flex; 
                    align-items: center; 
                    justify-content: center;
                    height: 100%;
                    width: 100%;
                    font-size: 30px; 
                    font-family: arial;
                    font-weight: bold;
                "
            >
                Hello, from scans.backend (API Server)!
            </div>
        """
    
    # 
    # GET /ping 
    # 
    @app.route("/ping")
    def ping():
        return "PONG"

    #
    # GET /mock-client
    # 
    @app.route("/mock-client")
    def mock_client(): 
        return send_file("./static/mock-client.html")

    #
    # GET /analyze 
    # 
    @app.route("/analyze")
    def analyze(): 
        
        # get arguments 
        task_id = str(uuid.uuid4())
        stream_ids = request.args.get("streams").split(",")  

        # process stream id 
        def process(): 
            TaskManager.process(task_id, stream_ids) 
        
        thread = Thread(target=process) 
        thread.run()

        # build response 
        data = {
            "task_id" : task_id, 
            "status"  : "SUBMITTED", 
            "stream_ids" : stream_ids
        }
        
        return data

    #
    # DEV ROUTES
    # 
    if os.getenv("ENV_MODE") == "dev": 
        #
        # GET /active-tasks 
        # 
        @app.route("/active-tasks")
        def active_tasks(): 
            from scans.core.TaskManager import TaskManager
            tasks = {} 
            for task_id in TaskManager.active_tasks: 
                task = TaskManager.active_tasks[task_id].load() 

                tasks[task_id] = {
                    "task_id" : task["task_id"],
                    "created_at" : task["created_at"], 
                    "stream_ids" : task["stream_ids"], 
                    "status" : task["status"]
                } 
            return tasks

        #
        # GET /active-rooms
        # 
        @app.route("/active-rooms")
        def active_rooms(): 
            from scans.core.TaskManager import TaskManager
            rooms = list(TaskManager.active_rooms.keys())
            return rooms