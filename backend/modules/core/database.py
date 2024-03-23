#
# :: database.py 
# Central file for connecting to database 
# 
from pymongo import MongoClient
import os 

#
# Connect to database and expose a database 
# connection object.
# 

# extract variables 
username = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")
host = os.getenv("MONGODB_HOST") 
port = os.getenv("MONGODB_PORT")

# build connection url
conn_url = \
    "mongodb://" + username + ":" + password + \
    "@" + host + ":" + port

# create connection object
database = os.getenv("MONGODB_DATABASE")
db_base = MongoClient(conn_url)
db = db_base[database]