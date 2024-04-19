#
# :: cache.py
# Centralized connection file for Redis.
# 
from redis import Redis
import os 

# get environment data  
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

# create redis instance 
redis = Redis(
    host=REDIS_HOST, 
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=0,
    decode_responses=True
) 
