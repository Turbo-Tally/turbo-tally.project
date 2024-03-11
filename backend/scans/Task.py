from datetime import date 

from .DAL import dal

class Task: 
    def __init__(self, task_id): 
        self.task_id = task_id

    def create(self, stream_ids):
        dal.models["tasks"].create({
            "task_id" : self.task_id, 
            "stream_ids" : stream_ids, 
            "status" : "PREPROCESSING", 
            "created_at" : str(date.today())
        }) 

    def update(self, status): 
        dal.models["tasks"].update(self.task_id, {
            "status" : status
        }) 