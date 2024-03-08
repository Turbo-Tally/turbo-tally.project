from scans.data.DataWrapper import DataWrapper

from scans.core.Task import Task
from scans.core.Stream import Stream

from time import time

class TaskManager:
    active_tasks = {}
    active_streams = {}
    active_rooms = {}

    def process(task_id, stream_ids): 
        """
            Code to create new task for stream ids.
        """ 

        # notify that the task is being processed
        output = f"> TaskManager: Processing task_id [{task_id}] \n"
        i = 0
        for stream_id in stream_ids:
            output += f"\tstream {i + 1} => [{stream_id}]\n"
            i += 1 

        print(output)

        # create task record in mongodb 
        print(f"> Creating task record for [{task_id}]...")
        DataWrapper.of("tasks").create({
            "task_id" : task_id, 
            "stream_ids" : stream_ids,
            "status" : "RUNNING", 
            "created_at" : time()
        })
        print(f"> Created task record for [{task_id}].")

        # register task 
        TaskManager.active_tasks[task_id] = Task.create(task_id) 
        TaskManager.active_tasks[task_id].streams = stream_ids
        
        # register streams 
        for stream_id in stream_ids: 
            TaskManager.active_streams[stream_id] = Stream.create(stream_id)

