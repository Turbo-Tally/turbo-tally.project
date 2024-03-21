#
# :: authentication.py 
# Authentication module.
# 
from hashlib import sha256
import os

class Authentication: 
    def hash(self, item):
        key = os.getenv("APP_KEY")[0:17] + item
        return sha256(key.encode("utf-8")).hexdigest() 

auth = Authentication()