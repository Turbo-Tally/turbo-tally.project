import uuid 
from time import time
from datetime import date

from .VideoInfo import VideoInfo
from .DAL import dal
from .Task import Task

class TaskManager: 
    def __init__(self):
        self.flask_app = None 
        self.socket_io = None

        self.state = {
            "foo" : "bar"
        } 

        self.refs = {
            
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

    def dispose(): 
        pass 

task_manager = TaskManager() 