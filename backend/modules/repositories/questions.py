#
# :: questions.py 
# Repository for `questions` collection. 
# 
from modules.core.repository import Repository 

class Questions(Repository): 
    def __init__(self): 
        
        self.collection_name = "questions" 
        self.main_key        = "_id"

        Repository.__init__(self)

questions = Questions()