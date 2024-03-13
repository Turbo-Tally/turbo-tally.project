#
# :: repository.py 
# Wrapper classes for accessing collections.
# 
from .database import db as db_

class Repository: 
    def __init__(self, db = db_): 
        
        # database object
        self.db = db
         
        # collection object
        self.col = self.get_collection() 

        # create main index
        self.create_main_index()

    def get_collection(self):
        return getattr(self.db, self.collection_name)

    def create_main_index(self): 
        self.col.create_index(
            [(self.main_key, pymongo.TEXT)], 
            name="main_index"
        )


