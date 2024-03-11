import pymongo

class DataModel: 
    def __init__(self, dal, collection, main_key, index_type = pymongo.TEXT): 
        self.dal = dal 
        self.collection = collection 
        self.main_key = main_key 

        self.context = getattr(self.dal.db, collection)

        self.context.create_index(
            [(self.main_key, index_type)], 
            name = "main_key"
        )
    
    def create(self, data): 
        return self.context.insert_one(data).inserted_id 

    def read(self, key):
        exists = self.exists(key)

        if not exists: 
            return None

        return self.context.find_one({ self.main_key : key }) 

    def update(self, key, data): 
        exists = self.exists(key) 

        if not exists: 
            raise Exception("Document not found.")

        return self.context.update_one(
            { self.main_key : key }, 
            { "$set" : data }
        )

    def exists(self, key): 
        count = self.context.count_documents(
            { self.main_key : key }, 
            limit = 1
        )

        if count == 0: 
            return False 
        else: 
            return True 

    def upsert(self, key, data): 
        exists = self.exists(key)

        if not exists: 
            raise Exception("Document not found.")

        if exists: 
            self.update(key, data)
        else: 
            return self.create(key, data)


    def delete(self, key): 
        exists = self.exists(key) 

        if not exists: 
            raise Exception("Document not found.") 
        
        self.delete_one({ self.main_key : key  })

