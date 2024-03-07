from pymongo import MongoClient 

class DAL: 
    connection = MongoClient(
        "mongodb://root:password@scans.database"
    )

    def init(): 
        scans = DAL.connection["scans"] 
        variables = scans.variables 
        variables.insert_one({ "key": "foo", "value": "bar" })

    def generic_store(table, message, data): 
        pass 

    def generic_insert(table, data): 
        pass 

    def generic_update(table, id_field, id_val, data): 
        pass 

    def store_message(message_id, data): 
        pass 
    
    def store_fetch_state(stream_id, data): 
        pass 
    
    def store_report(stream_id, data):
        pass 

    def store_exchange_rates(data):
        pass 

    def get_message(message_id): 
        pass 
    
    def get_fetch_state(stream_id):
        pass 
    
    def get_report(message_id):
        pass 

    def get_exchange_rates(date): 
        pass     

    