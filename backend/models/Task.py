
class Task: 
    def __init__(self, task_id): 
        self.task_id = task_id 
    
    def from_task_id(self, task_id): 
        task = Task(task_id) 
        return task 
    
    def get_stream_ids(self): 
        pass 
    
    def get_categorized_streams(self): 
        pass 