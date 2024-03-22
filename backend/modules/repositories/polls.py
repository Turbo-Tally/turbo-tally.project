#
# :: polls.py 
# Polls repository 
# 
from modules.core.repository import Repository 

class Polls(Repository): 
    def __init__(self): 
        
        self.collection_name = "polls" 
        self.main_key        = "_id"    

        Repository.__init__(self)
        

polls = Polls()