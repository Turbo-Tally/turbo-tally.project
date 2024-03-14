#
# :: messages.py 
# Repository for `messages` collection.
#  
from scans.core.repository import Repository 

class Messages(Repository): 
    def __init__(self): 
        
        self.collection_name = "messages" 
        self.main_key        = "message_id"

        Repository.__init__(self)

    
messages = Messages()