from scans.data.DataWrapper import DataWrapper

class Stream: 
    def __init__(self, stream_id): 
        self.stream_id = stream_id

    def create(stream_id): 
        stream = Stream(stream_id)
        return stream 

    def load(self): 
        return DataWrapper.of("streams").read(self.stream_id) 
    
    def save(self, data): 
        DataWrapper.of("streams").update(self.stream_id, data)
