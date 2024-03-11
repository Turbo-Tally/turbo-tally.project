import uuid 
from .VideoInfo import VideoInfo

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

        # get information of videos 
        infos = {} 
        for stream_id in stream_ids: 
            info = VideoInfo(stream_id) 
            infos[stream_id] = {
                "title" : info.title, 
                "channel" : info.channel, 
                "channel_id" : info.channel_id
            }

        return task_id, infos

    def dispose(): 
        pass 

task_manager = TaskManager() 