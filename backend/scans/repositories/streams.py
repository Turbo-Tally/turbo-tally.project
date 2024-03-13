#
# :: streams.py 
# Repository for `streams` objects. 
#  
from scans.core.repository import Repository 

class Streams(Repository):    
    def __init__(self): 
        
        self.collection_name = "streams" 
        self.main_key        = "stream_id"

        Model.__init__(self)

streams = Streams()