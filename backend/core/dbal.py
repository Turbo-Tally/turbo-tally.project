from pymongo import MongoClient 

class DBAL: 
    connection = MongoClient(
        "mongodb://root:password@scans.database"
    )

    def init(): 
        scans = DBAL.connection["scans"] 
        variables = scans.variables 
        variables.insert_one({ "key": "foo", "value": "bar" })



    