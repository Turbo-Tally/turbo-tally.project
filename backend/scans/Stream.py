from .DAL import dal
from random import randint
from threading import Thread

from scans.TaskManager import task_manager

class Stream: 
    def __init__(self, stream_id):
        self.stream_id = stream_id 
        self.collector_thread = None 
        self.analyzer_thread = None 
    
    def clear(self): 
        print(f"@ Clearing stream ({self.stream_id})...")
        thread = task_manager.threads["streams"][self.stream_id] 
        thread.join() 
        del task_manager.threads["streams"][self.stream_id] 

    def runner(self, socket_io): 
        # create collector and analyzer object
        collector = Collector(self.stream_id) 
        analyzer = Analyzer(self.stream_id)

        # create threads for collector and analyzer 
        

        while True: 
            print(
                f"> stream.runner : Stream [{self.stream_id}]" +
                f"-> ({ randint(1, 100)})"
            )
            socket_io.sleep(1) 
        pass