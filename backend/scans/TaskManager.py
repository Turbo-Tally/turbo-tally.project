import uuid 
from time import time
from datetime import date

from .VideoInfo import VideoInfo
from .DAL import dal
from .Task import Task
from .Stream import Stream

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
            
            "collector" : {
                # collector threads
            }, 

            "analyzer" : {
                # analyzer threads
            }
        }

    def preprocess(self, stream_ids): 
        task_id = str(uuid.uuid4())
        
        # create initial record for the task
        task = Task(task_id)
        task.create(stream_ids)

        # preprocessing (just in case)
        # ...

        # update task
        task.update("PREPROCESSED")

        return task_id

    def dispose(self): 
        # clear streams state 
        def on_clear_stream(stream_id):
            Stream(stream_id).clear()

        self.clear_empties(self.state["streams"], on_clear_stream)

        # clear tasks state 
        def on_clear_task(task_id):
            Task(task_id).clear()

        self.clear_empties(self.state["tasks"], on_clear_task)

    def clear_empties(self, items, on_clear_item): 
        to_delete = [] 

        for key in items:
            count = len(items[key].keys())
            if count == 0: 
                to_delete.append(key)
      
        for key in to_delete: 
            on_clear_item(key)
            del items[key]

task_manager = TaskManager() 