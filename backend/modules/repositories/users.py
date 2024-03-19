#
# :: users.py 
# Repository for `users` collection. 
# 
from scans.core.repository import Repository 

class Users(Repository): 
    def __init__(self): 
        
        self.collection_name = "users" 
        self.main_key        = "_id"

        Repository.__init__(self)

users = Users()