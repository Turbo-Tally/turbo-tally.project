#
# :: auto_increments.py 
# Answers repository 
# 
from modules.core.repository import Repository 

class AutoIncrements(Repository): 
    def __init__(self): 
        
        self.collection_name = "auto_increments" 
        self.main_key        = "_id"    

        Repository.__init__(self)

    def init(self, key): 
        if self.exists(key): 
            return 

        print(f"> Initializing [{key}]")

        self.create({
            "_id" : key, 
            "counter" : 0 
        })

    def next(self, key): 
        self.coll.update_one(
            { "_id" : key }, 
            { "$inc" : { "counter" : 1 } }
        )
        counter = self.read(key)["counter"]
        return counter
    
auto_increments = AutoIncrements()