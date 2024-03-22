#
# :: choices.py 
# Choices repository 
# 
from modules.core.repository import Repository 

class Choices(Repository): 
    def __init__(self): 
        
        self.collection_name = "choices" 
        self.main_key        = "_id"    

        Repository.__init__(self)
        
        # create indices for this repository
        self.coll.create_index("poll.$id", name="poll_id")

choices = Choices()