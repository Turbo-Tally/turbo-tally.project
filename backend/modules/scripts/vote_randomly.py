# 
# CLEAR VOTES OF POLL 
# 
import utils.preloader 
import sys 
import os
import random
import socketio
from time import sleep
from bson.json_util import dumps

from modules.repositories.users import users 
from modules.main.voting import Voting 
from modules.main.analysis import Analyzer 

poll_id = int(sys.argv[1])

n_users = 1000

def get_random_users(amount):
    user_list = list(users.coll.aggregate([
        { "$sample" : { "size" : amount } }
    ])) 
    return user_list 

def random_choice(choices): 
    return random.choice(choices)

users = get_random_users(n_users)

sio = socketio.SimpleClient()
sio.connect('http://172.28.2.3:80')


for user in users:
    choices = Analyzer.choices(poll_id)
    choice = random_choice(choices)
    print(f"User {user['_id']} is answering [{choice}]...")

    Voting.answer_poll(user, {
        "poll_id" : poll_id, 
        "answer" : choice
    })

    sio.emit("forward", {
        "key" : os.getenv("APP_SECRET"),
        "room" : f"poll.{poll_id}", 
        "event" : "should-update", 
        "data" : int(poll_id)
    })

    sio.emit("forward", {
        "key" : os.getenv("APP_SECRET"), 
        "room" : "recent-answers",
        "event" : "new-update", 
        "data" : dumps(Voting.recent_answers())
    })

    sleep(60 / n_users)