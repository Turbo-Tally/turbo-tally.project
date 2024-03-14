#
# :: channels.py 
# Repository for `channels` collection. 
# 
from scans.core.repository import Repository 

class Channels(Repository): 
    def __init__(self): 
        
        self.collection_name = "channels" 
        self.main_key        = "channel_id"

        Repository.__init__(self)

    def streamExistsIn(self, stream_id, channel_id): 
        return self.coll.find_one({ 
            "stream_list." + stream_id : { "$exists" : True }
        }) is not None


channels = Channels()