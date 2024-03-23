#
# :: voting.py 
# Voting module. 
# 
from bson.objectid import ObjectId

from modules.repositories.polls import polls
from modules.repositories.answers import answers
from modules.repositories.choices import choices

from datetime import datetime
from modules.common.formats import datetime_format
from modules.core.database import db_base

class Voting: 
    def create_poll(user, data):
        with db_base.start_session() as session:
            # create normalized data 
            poll_id = polls.next_id() 

            norm_data = {
                "_id" : poll_id,
                "title" : data["title"],
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
            inserted_id = \
                polls.coll.insert_one(norm_data, session=session).inserted_id

            # create records for choices 
            choice_list = data["choices"] 
            choice_records = []

            for choice in choice_list: 
                choice_records.append({
                    "_id" : choices.next_id(), 
                    "poll" : {
                        "$ref" : "polls", 
                        "$id" : poll_id 
                    }, 
                    "answer" : choice
                })

            choices.coll.insert_many(choice_records, session=session)

            return inserted_id

    def answer_poll(user, data): 
        with db_base.start_session() as session:
            user_id = int(user["_id"]) 
            poll_id = int(data["poll_id"])   

            # create normalized data
            norm_data = {
                "_id" : answers.next_id(),
                "user" : {
                    "$ref" : "users", 
                    "$id" : user_id 
                }, 
                "poll" : {
                    "$ref" : "polls", 
                    "$id" : poll_id
                },
                "answer" : data["answer"]
            }

            # create poll record 
            inserted_id = \
                answers.coll.insert_one(norm_data, session=session).inserted_id

            # create choice record if not yet exists 
            if choices.coll.find_one({
                "poll.$id" : poll_id, 
                "answer" : data["answer"]
            }) is None: 
                choices.coll.insert_one({
                    "_id" : choices.next_id(), 
                    "poll" : {
                        "$ref" : "polls", 
                        "$id" : poll_id
                    },
                    "answer" : data["answer"]
                }, session=session)

            return inserted_id 
        

    def browse_polls(query, sort, filter_, cursor, **kwargs): 
        if filter_ == "all": 
            sorted_polls = polls.coll.find({
                "title" : { "$regex" : query }, 
            })

        elif filter_ == "answered": 
            sorted_polls = polls.coll.find({
                "title" : { "$regex" : query }, 
            })

        elif filter_ == "unanswered": 
            sorted_polls = polls.coll.find({
                "title" : { "$regex" : query }, 
            })

        else: 
            raise Exception("Unknown filter mode [" + filter_ + "].")  

        return sorted_polls

    def get_poll_choices(poll_id): 
        choice_list = choices.coll.find({
            "poll.$id" : poll_id 
        })
        return choice_list

    def find_in_choices(poll_id, q): 
        choice_list = choices.coll.find({
            "poll.$id" : poll_id, 
            "answer" : { "$regex" : q }
        })
        return choice_list

    def clear_polls():
        polls.coll.drop()  

voting = Voting()