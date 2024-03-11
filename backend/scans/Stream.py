from .DAL import dal

class Stream: 
    def __init__(self, stream_id):
        self.stream_id = stream_id 
    
    def clear(self): 
        thread = dal.threads["streams"][self.stream_id] 
        thread.join() 
        del dal.threads["streams"][self.stream_id] 