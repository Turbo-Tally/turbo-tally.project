from pymongo import MongoClient
import os 

class DAL: 
    def __init__(self, **kwargs): 
        self.host = kwargs.get("host") 
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.database = kwargs.get("database")
        self.port = kwargs.get("port") 
        
        self.db = None
        
        self.connect()

        self.models = {}

    def connect(self): 
        host = self.host 
        username = self.username 
        password = self.password 
        database = self.database 
        port = self.port 

        self.db = MongoClient(
            f"mongodb://{username}:{password}@{host}:{port}"
        )[self.database]


dal = DAL(
    host = os.getenv("MONGODB_HOST"), 
    port = os.getenv("MONGODB_PORT"),
    username = os.getenv("MONGODB_USERNAME"), 
    password = os.getenv("MONGODB_PASSWORD"), 
    database = os.getenv("MONGODB_DATABASE")
)