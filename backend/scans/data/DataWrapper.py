import os 
from pymongo import MongoClient



class DataWrapper:
    wrappers = {} 

    def __init__(self, collection, main_key): 
        self._collection = collection 
        self._main_key = main_key 

    def of(collection): 
        return DataWrapper.wrappers[collection] 
    
    def register(collection, key): 
        DataWrapper.wrappers[collection] = DataWrapper(collection, key)

    def db():
        return DataWrapper.connection()["scans"]
    
    def connection():
        MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
        MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
        MONGODB_HOST = os.getenv("MONGODB_HOST")
        MONGODB_PORT = os.getenv("MONGODB_PORT")

        return MongoClient(
            f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}" + 
            f"@{MONGODB_HOST}:{MONGODB_PORT}/"
        )

    def collection(self):
        return getattr(DataWrapper.db(), self._collection)
    
    def create(self, data): 
        collection = self.collection() 
        inserted_id = collection.insert_one(data).inserted_id 
        return inserted_id 
    
    def update(self, key, data): 
        collection = self.collection() 
        collection.update_one({ self._main_key : key }, { "$set" : data }) 
    
    def read(self, key): 
        collection = self.collection() 
        return collection.find_one({ self._main_key : key })

    def upsert(self, key, data): 
        collection = self.collection() 
        if self.read(key) is None: 
            self.create(data)
        else:   
            self.update(key, data)

    def remove(self, key): 
        collection = self.collection() 
        collection.delete_one({ self._main_key : key }) 

