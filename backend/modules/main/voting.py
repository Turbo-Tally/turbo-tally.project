#
# :: voting.py 
# Voting module. 
# 
from bson.objectid import ObjectId

from modules.repositories.polls import polls
from modules.repositories.answers import answers

from datetime import datetime
from modules.common.formats import datetime_format

class Voting: 
    def create_poll(user, data):
        # create normalized data
        norm_data = {
            "info" : {
                "title" : data["title"], 
                "choices" : data["choices"]
            }, 
            "user" : {
                "$ref" : "users", 
                "$id" : user["_id"]
            }, 
            "meta" : {

            },
            "chart_data" : {

            }, 
            "bot_flags" : {
                "is_locked" : False
            },
            "created_at" : datetime.now().strftime(datetime_format)
        } 

        # insert poll in database 
        inserted_id = polls.create(norm_data)

        return inserted_id

    def answer_poll(user, data): 
        user_id = user["_id"]    

        # get poll choices 
        poll = polls.coll.find_one({ 
            "_id" : ObjectId(data["poll_id"])
        })
             
        has_answer = polls.coll.find_one({ 
            "info.choices" : data["answer"]
        })
             

        # create normalized data
        norm_data = {
            "user" : {
                "$ref" : "users", 
                "$id" : user_id 
            }, 
            "poll" : {
                "$ref" : "polls", 
                "$id" : ObjectId(data["poll_id"])
            },
            "answer" : data["answer"]
        }

        # add to poll choices if does not yet exist 
        if has_answer is None: 
            polls.coll.update_one(
                { "_id" : ObjectId(data["poll_id"]) }, 
                {
                    "$push" : {
                        "info.choices" : data["answer"]
                    }
                }
            )

        # create poll record 
        answers.create(norm_data)

    def browse_polls(query, sort, filter_, cursor, **kwargs): 
        if filter_ == "all": 
            sorted_polls = polls.coll.find({
                "info.title" : { "$regex" : query }, 
            })

        elif filter_ == "answered": 
            sorted_polls = polls.coll.find({
                "info.title" : { "$regex" : query }, 
            })

        elif filter_ == "unanswered": 
            sorted_polls = polls.coll.find({
                "info.title" : { "$regex" : query }, 
            })

        else: 
            raise Exception("Unknown filter mode [" + filter_ + "].")  

        return sorted_polls

    def clear_polls():
        polls.coll.drop()  

voting = Voting()