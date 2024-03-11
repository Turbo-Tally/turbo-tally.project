from flask import request 
from flask_socketio import emit, send, join_room, leave_room
from time import time

from scans.TaskManager import task_manager
from scans.DAL import dal

def make_ws_api(socket_io):

    @socket_io.on("connect")
    def on_connect(): 
        sid = request.sid
        task_id = request.args.get("task_id")
        timestamp = time()

        print(f"> Client connected    -> SID: [{sid}].")

        # record entry of client
        task_manager.state["clients"][sid] = {
            "join_time" : timestamp, 
            "task_id" : task_id
        }

        # back reference tasks to client id 
        if task_id not in task_manager.state["tasks"]: 
            task_manager.state["tasks"][task_id] = {} 
        task_manager.state["tasks"][task_id][sid] = timestamp
        
        # back reference streams to client id 
        task = dal.models["tasks"].read(task_id)
        stream_ids = task["stream_ids"]
        for stream_id in stream_ids:
            if stream_id not in task_manager.state["streams"]:
                task_manager.state["streams"][stream_id] = {} 
            task_manager.state["streams"][stream_id][sid] = timestamp 


    @socket_io.on("disconnect")
    def on_disconnect():
        sid = request.sid 
        task_id = task_manager.state["clients"][sid]["task_id"]

        print(f"> Client disconnected -> SID: [{sid}].")

        # remove record in client state 
        del task_manager.state["clients"][sid] 

        # remove record in tasks state if needed 
        del task_manager.state["tasks"][task_id][sid]

        # remove record in back reference of streams to sockets 
        task = dal.models["tasks"].read(task_id)
        stream_ids = task["stream_ids"] 
        for stream_id in stream_ids: 
            del task_manager.state["streams"][stream_id][sid]

        # perform general disposition tasks of task manager 
        task_manager.dispose()
        