#
# :: repository.py 
# Wrapper classes for accessing collections.
# 
import pymongo
from .database import db as db_

class Repository: 
    def __init__(self, db = db_): 
        
        # database object
        self.db = db
         
        # collection object
        self.coll = getattr(self.db, self.collection_name)

        # create main index
        self.create_main_index()

    def create_main_index(self, **kwargs):
        index_type = kwargs.get("index_type", pymongo.TEXT) 
        self.coll.create_index(
            [(self.main_key, index_type)], 
            name="main_index"
        )

    def create(self, data): 
        insert_id = self.coll.insert_one(data).inserted_id 
        return insert_id 

    def read(self, key_value): 
        return self.coll.find_one({ self.main_key : key_value })

    def exists(self, key_value): 
        return self.read(key_value) is not None

    def update(self, key_value, data): 
        self.coll\
            .update_one(
                { self.main_key : key_value }, 
                { "$set" : data}
            ) 

    def upsert(self, key_value, data): 
        if self.coll.exists(key_value): 
            self.create(data)
        else: 
            self.update(key_value, data) 

    def delete(self, key_value): 
        self.coll\
            .delete_one(key_value)

    def count_all(self): 
        return self.coll.count_documents({})