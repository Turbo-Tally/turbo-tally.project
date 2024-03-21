#
# :: variables.py 
# Repository for `variables` collection. 
# 
from modules.core.repository import Repository 

class Variables(Repository): 
    def __init__(self): 
        
        self.collection_name = "variables" 
        self.main_key        = "_id"

        Repository.__init__(self)


variables = Variables()