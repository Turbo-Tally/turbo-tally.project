import redis 

class Cache: 
    client = redis.Redis(
        host="scans.cache", 
        port="6379", 
        decode_responses=True, 
        password="password"
    )   

    def init():
        pass 