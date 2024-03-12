from .DAL import dal
from random import randint
from threading import Thread

from scans.TaskManager import task_manager
from scans.Collector import Collector
from scans.Analyzer import Analyzer

class Stream: 
    def __init__(self, stream_id):
        self.stream_id = stream_id 
        self.switch = True 

    
    def clear(self): 
        print(f"@ Clearing stream ({self.stream_id})...")
        
        self.switch = False

        thread = task_manager.threads["streams"][self.stream_id] 
        thread.join()
         
        del task_manager.threads["streams"][self.stream_id] 


        task_manager.refs["collectors"][self.stream_id].clear() 
        task_manager.refs["analyzers"][self.stream_id].clear()


    def create_subthreads(self, socket_io): 
        # create collector and analyzer objects
        collector = Collector(self.stream_id) 
        analyzer = Analyzer(self.stream_id) 

        task_manager.refs["collectors"][self.stream_id] = collector
        task_manager.refs["analyzers"][self.stream_id] = analyzer

        # create threads for collector and analyzer 
        collector_thread = \
            Thread(target=collector.runner, args=(socket_io,))
        task_manager.threads["collectors"][self.stream_id] = \
            collector_thread

        analyzer_thread = \
            Thread(target=analyzer.runner, args=(socket_io,))
        task_manager.threads["analyzers"][self.stream_id] = \
            analyzer_thread

        collector_thread.start()
        analyzer_thread.start()
 

    def runner(self, socket_io): 
        # create subthreads 
        self.create_subthreads(socket_io) 

        while True:
            print(
                f"> stream.runner : Stream [{self.stream_id}]" +
                f"-> ({ randint(1, 100)})"
            )
            print("\t-> Stream Switch :", self.switch)

            socket_io.sleep(1) 

            if not self.switch:
                break

        pass