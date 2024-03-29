#
# :: answers.py 
# Answers repository 
# 
from modules.core.repository import Repository 
from .auto_increments import auto_increments

class Answers(Repository): 
    def __init__(self): 
        
        self.collection_name = "answers" 
        self.main_key        = "_id"    
        
        Repository.__init__(self)
        
        # create indices for this repository
        self.coll.create_index("user.$id", name="user_id")
        self.coll.create_index("poll.$id", name="poll_id")

answers = Answers()