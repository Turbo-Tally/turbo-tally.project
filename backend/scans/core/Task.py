from scans.data.DataWrapper import DataWrapper

class Task: 
    def __init__(self, task_id):
        self.task_id = task_id
        self.streams = {}

    def create(task_id): 
        task = Task(task_id) 
        return task 

    def add_stream(stream_id, stream):
        self.streams[stream_id] = stream 

    def load(self): 
        return DataWrapper.of("tasks").read(self.task_id)

    def save(self, data): 
        DataWrapper.of("tasks").update(self.task_id, data)

    