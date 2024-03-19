#
# :: answers.py 
# Answers repository 
# 

class Answers(Repository): 
    def __init__(self): 
        
        self.collection_name = "answers" 
        self.main_key        = "_id"    

        Repository.__init__(self)
        
        # create indices for this repository
        self.coll.create_index("user._id", name="user_id")
        self.coll.create_index("poll._id", name="poll_id")

questions = Answers()