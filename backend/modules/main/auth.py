#
# :: authentication.py 
# Authentication module.
# 
from hashlib import sha256
from random import randint
from datetime import datetime, timedelta
import os
from bson.objectid import ObjectId

from modules.common.formats import datetime_format

from modules.repositories.verif_codes import verif_codes
from modules.repositories.users import users

from modules.core.cache import redis

class Authentication: 
    def hash(self, item):
        key = os.getenv("APP_KEY")[0:17] + item
        return sha256(key.encode("utf-8")).hexdigest() 

    def generate_verif_code(self): 
        expiration_time = datetime.now() + timedelta(minutes=15) 
        code = "" 
        for i in range(6): 
            code += str(randint(0, 6)) 
        return code, expiration_time

    def register_verif_code(self, type_, handle, code, expiration_time): 
        verif_codes.upsert(handle, {
            "type" : type_, 
            "handle" : handle, 
            "code" : code,
            "expires_at" : expiration_time
        })

    def check_verif_code(self, handle, code): 
        verif_code = verif_codes.read(handle) 

        if verif_code is None: 
            return False
        
        if verif_code["expires_at"] < datetime.now():
            return False 
        
        if verif_code["code"] != code: 
            return False
        
        return True

    def clear_verif_code(self, handle):
        verif_codes.delete(handle)

    def create_user(self, data): 
        users.create(data)

    def check_if_user_already_exists_by(self, field, value): 
        return (
            users.coll.find_one({
                field: value
            }) is not None
        )

    def set_session_user(self, session_id, user_id): 
        redis.hset(f"users", session_id, user_id)

    def get_session_user(self, session_id): 
        user_id = redis.hget(f"users", session_id)
        return users.coll.find_one({ "_id" : ObjectId(user_id) })

    def clear_session_user(self, session_id): 
        redis.hdel("users", session_id)

    def find_user_by_email(self, email): 
        return users.coll.find_one({ "auth.email" : email })

auth = Authentication()