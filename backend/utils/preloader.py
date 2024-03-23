#
# :: preloader.py
# Preload other modules needed before other scripts 
# 

# load dotenv
from dotenv import load_dotenv 
load_dotenv(".env")

# load formats and validators
import modules.common.formats 

# preload default 
def preload_default(): 
    initialize_auto_increments() 
    create_admin_user()

# create auto-incrementers 
def initialize_auto_increments():

    from modules.repositories.auto_increments import auto_increments

    auto_increments.init("answers")
    auto_increments.init("choices")
    auto_increments.init("counters") 
    auto_increments.init("polls") 
    auto_increments.init("users")
    auto_increments.init("variables") 
    auto_increments.init("verif_codes")

# create admin user 
def create_admin_user(): 
    from modules.repositories.users import users 
    from modules.main.auth import auth
    from datetime import datetime
    from modules.common.formats import datetime_format

    if users.coll.find_one({ "auth.username" : "admin" }) is None:
        auth.create_user({
            "info" : {
                "birthdate" : "2000-01-01 00:00:00",
                "gender" : "M", 
                "region" : "V",
                "province" : "CAS",
                "mobile_no" : "09000000000"
            }, 
            "auth" : {
                "username" : "admin",
                "email" : "admin@example.com", 
                "password" : "password",
                "password_hash" : auth.hash("password"),
                "is_admin" : False, 
                "is_bot" : False
            },
            "created_at" : datetime.now().strftime(datetime_format), 
            "updated_at" : None
        })

