#
# SETUP WEBSOCKETS
# 
from flask import request
from flask_socketio import join_room, send, emit
from scans.data.VideoInfo import VideoInfo

from scans.core.TaskManager import TaskManager
from scans.rooms.StreamRoom import StreamRoom 
from scans.rooms.TaskRoom import TaskRoom

def setup_websockets(socket_io): 

    @socket_io.on("connect") 
    def connect(): 
        # get socket id 
        sid = request.sid 
        
        # output to console status of new connection
        print(f"> Received connection from socket_id [{sid}]")

    @socket_io.on("gen_sync") 
    def on_gen_syc(data): 
        sid = request.sid 

        task_id = data["task_id"]
        stream_ids = data["stream_ids"]

        # sync task id 
        print("SID:", sid, "Task ID:", task_id)
        TaskManager.sid_task_id[sid] = task_id

        # sync stream ids 
        print("Stream IDs : ", stream_ids)
        for stream_id in stream_ids: 
            if stream_id not in TaskManager.stream_refs:
                TaskManager.stream_refs[stream_id] = {}
            TaskManager.stream_refs[stream_id][task_id] = True


    @socket_io.on("join_room")
    def on_join(data): 
        room_id = data
        sid = request.sid 
        
        print(f"> Received signal for [{sid}] to join room {room_id}")
        
        # join room 
        join_room(room_id)
        emit("joined_room", room_id)

        # determine room type 
        room_type = room_id.split(".")[0] 

        # create room based on room type 
        if room_id not in TaskManager.active_rooms:
            room = None 
            
            if room_type == "stream": 
                room = StreamRoom(room_id, socket_io).run()
            elif room_type == "task": 
                room = TaskRoom(room_id, socket_io).run()

            TaskManager.active_rooms[room_id] = room
       
    @socket_io.on("get_video_infos")
    def on_get_video_infos(data): 
        video_ids = data 
        video_infos = {}
        sid = request.sid

        print(
            f"> Received signal for [{sid}] to " + 
            f"get video information {video_ids}"
        )

        for video_id in video_ids: 
            video_info = VideoInfo(video_id) 
            video_infos[video_id] = {
                "stream_id" : video_id,
                "title" : video_info.title, 
                "channel" : video_info.channel 
            }
        
        emit("video_infos", video_infos)

    @socket_io.on("disconnect") 
    def on_disconnect(): 
        sid = request.sid

        task_id = TaskManager.sid_task_id[sid]
        stream_ids = TaskManager.active_tasks[task_id].streams

        print("Disconnect Task ID :", task_id)
        print("Disconnect Stream IDs :", stream_ids)

        if "task." + task_id in TaskManager.active_rooms:
            del TaskManager.active_rooms["task." + task_id]
        
        if task_id in TaskManager.active_tasks: 
            del TaskManager.active_tasks[task_id]

        if task_id in TaskManager.sid_task_id:
            del TaskManager.sid_task_id[sid] 

        for stream_id in stream_ids: 
            del TaskManager.stream_refs[stream_id][task_id]
        
        print("> Client disconnected...")




