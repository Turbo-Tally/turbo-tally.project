#
# :: questions.py 
# Repository for `questions` collection. 
# 
from scans.core.repository import Repository 

class Questions(Repository): 
    def __init__(self): 
        
        self.collection_name = "questions" 
        self.main_key        = "question_id"

        Repository.__init__(self)

questions = Questions()