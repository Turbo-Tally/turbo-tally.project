from .DAL import dal
from random import randint
from threading import Thread

from scans.TaskManager import task_manager
from scans.Collector import Collector
from scans.Analyzer import Analyzer

class Stream: 
    def __init__(self, stream_id):
        self.stream_id = stream_id 

    
    def clear(self): 
        print(f"@ Clearing stream ({self.stream_id})...")
        thread = task_manager.threads["streams"][self.stream_id] 
        thread.join() 
        del task_manager.threads["streams"][self.stream_id] 
        task_manager.threads["collectors"].clear() 
        task_manager.threads["analyzers"].clear()
 

    def runner(self, socket_io): 
        # create collector and analyzer object
        collector = Collector(self.stream_id) 
        analyzer = Analyzer(self.stream_id)

        # create threads for collector and analyzer 
        collector_thread = \
            Thread(target=collector.runner, args=(socket_io,))
        task_manager.threads["collectors"][self.stream_id] = \
            collector_thread

        analyzer_thread = \
            Thread(target=analyzer.runner, args=(socket_io,))
        task_manager.threads["analyzers"][self.stream_id] = \
            analyzer_thread

        self.collector_thread.start()
        self.analyzer_thread.start()

        # while True: 
        #     print(
        #         f"> stream.runner : Stream [{self.stream_id}]" +
        #         f"-> ({ randint(1, 100)})"
        #     )
        #     socket_io.sleep(1) 
        pass