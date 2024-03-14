#
# :: streams.py 
# Repository for `streams` objects. 
#  
from scans.core.repository import Repository 

class Streams(Repository):    
    def __init__(self): 
        
        self.collection_name = "streams" 
        self.main_key        = "stream_id"

        Repository.__init__(self)
    
    def blank(self, video_id, channel_id):
        streams.create({
            "stream_id"  : video_id, 
            "channel_id" : channel_id, 
            "reports" : {

            }, 
            "timestamps" : {
                "created_at" : time(), 
                "updated_at" : None
            }
        })
        
streams = Streams()