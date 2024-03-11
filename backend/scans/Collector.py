from .DAL import dal
from scans.TaskManager import task_manager

class Collector: 
    def __init__(self, stream_id):   
        self.stream_id = stream_id 

    def clear(self): 
        thread = task_manager.threads["collectors"][self.stream_id] 
        thread.join() 
        del task_manager.threads["collectors"][self.stream_id] 

    def runner(self, socket_io): 
        while True: 
            print(f"> collector.runner : Stream [{self.stream_id}]")
            socket_io.sleep(1) 