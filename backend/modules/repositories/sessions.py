#
# :: sessions.py 
# Repository for `sessions` collection. 
# 
from modules.core.repository import Repository 

class Sessions(Repository): 
    def __init__(self): 
        
        self.collection_name = "verif_codes" 
        self.main_key        = "handle"

        Repository.__init__(self)

sessions = Sessions()