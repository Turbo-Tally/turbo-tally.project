#
# :: channels.py 
# Repository for `channels` collection. 
# 
from scans.core.repository import Repository 

class Channels(Repository): 
    def __init__(self): 
        
        self.collection_name = "channels" 
        self.main_key        = "channel_id"

        Model.__init__(self)

channels = Channels()