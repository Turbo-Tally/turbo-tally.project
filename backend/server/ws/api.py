from flask import request 
from flask_socketio import emit, send, join_room, leave_room, rooms
from time import time

from scans.TaskManager import task_manager
from scans.DAL import dal
from scans.Task import Task
from scans.Stream import Stream

def make_ws_api(socket_io):

    @socket_io.on("connect")
    def on_connect(): 
        sid = request.sid
        task_id = request.args.get("task_id")
        task = dal.models["tasks"].read(task_id)
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
        stream_ids = task["stream_ids"]
        for stream_id in stream_ids:
            if stream_id not in task_manager.state["streams"]:
                task_manager.state["streams"][stream_id] = {} 
            task_manager.state["streams"][stream_id][sid] = timestamp 

        ########################################
        # Create background threads and rooms. #
        ######################################## 

        # create task thread (if needed)
        if task_id not in task_manager.threads["tasks"]:
            task = Task(task_id)
            task_manager.refs["tasks"] [task_id] = task

            thread = \
                socket_io.start_background_task(task.runner, socket_io)
            
            task_manager.threads["tasks"][task_id] = thread
        
        # join task room
        task_room_id = "task." + task_id
        join_room(task_room_id)

        # create stream thread (if needed) 
        for stream_id in stream_ids: 
            stream = Stream(stream_id)
            task_manager.refs["streams"][stream_id] = stream
            
            if stream_id not in task_manager.threads["streams"]: 
                thread = \
                    socket_io.start_background_task(stream.runner, socket_io)
                task_manager.threads["streams"][stream_id] = thread 

            stream_room_id = "stream." + stream_id 
            join_room(stream_room_id) 

        # update task manager 
        task_manager.rooms[sid] = rooms(sid)





    @socket_io.on("disconnect")
    def on_disconnect():
        sid = request.sid 
        task_id = task_manager.state["clients"][sid]["task_id"]

        print(f"> Client disconnected -> SID: [{sid}].")

        # leave room 
        leave_room("task." + task_id)

        # remove record in client state 
        del task_manager.state["clients"][sid] 

        # remove record in tasks state if needed 
        del task_manager.state["tasks"][task_id][sid]

        # remove record in back reference of streams to sockets 
        task = dal.models["tasks"].read(task_id)
        stream_ids = task["stream_ids"] 
        for stream_id in stream_ids: 
            del task_manager.state["streams"][stream_id][sid]
            leave_room("stream." + stream_id)

        # perform general disposition tasks of task manager 
        task_manager.dispose()

        # update task manager 
        del task_manager.rooms[sid]