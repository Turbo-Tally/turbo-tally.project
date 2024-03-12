import uuid 
from time import time
from datetime import date

from .VideoInfo import VideoInfo
from .DAL import dal

class TaskManager: 
    def __init__(self):
        self.flask_app = None 
        self.socket_io = None

        self.state = {
            "clients" : {
                # mapping of client ids (SIDs) to task_id and join_time
            }, 

            "streams" : {
                # mapping of streams to client ids (SIDs)
            }, 

            "tasks" : {
                # mapping of tasks to client ids (SIDs)
            }
        } 

        self.threads = {
            "tasks" : {
                # task threads
            },

            "streams" : {
                # stream threads
            }, 
            
            "collectors" : {
                # collector threads
            }, 

            "analyzers" : {
                # analyzer threads
            }
        }

        self.refs = {
            "tasks" : {}, 
            "streams" : {}, 
            "collectors" : {}, 
            "analyzers" : {} 
        }

    def preprocess(self, stream_ids): 
        from .Task import Task

        task_id = str(uuid.uuid4())
        
        # create initial record for the task
        task = Task(task_id)
        task.create(stream_ids)

        # pre-processing (just in case)
        # ...

        # update task
        task.update("PREPROCESSED")

        return task_id

    def dispose(self): 
        from .Stream import Stream
        from .Task import Task

        # clear streams state 
        def on_clear_stream(stream_id):
            task_manager.refs["streams"][stream_id].clear()

        stream_dels = self.clear_empties(self.state["streams"])

        # clear tasks state 
        def on_clear_task(task_id):
            task_manager.refs["tasks"][task_id].clear()

        task_dels = self.clear_empties(self.state["tasks"])

        print("Stream Dels :", stream_dels)
        print("Task Dels :", task_dels)

        # clear threads
        for key in stream_dels: 
            on_clear_stream(key) 
        
        for key in task_dels: 
            on_clear_task(key)


    def clear_empties(self, items): 
        to_delete = [] 

        for key in items:
            count = len(items[key].keys())
            if count == 0: 
                to_delete.append(key)
      
        for key in to_delete: 
            del items[key]

        return to_delete

task_manager = TaskManager() 