#
# :: voting.py 
# Voting module. 
# 
from bson.objectid import ObjectId
from bson.json_util import dumps

from modules.repositories.polls import polls
from modules.repositories.answers import answers
from modules.repositories.choices import choices
from modules.repositories.users import users

from datetime import datetime
from modules.common.formats import datetime_format
from modules.core.database import db_base

import re

class Voting: 
    def create_poll(user, data, **kwargs):
        created_at = kwargs.get("created_at", datetime.now())

        with db_base.start_session() as session:
            # create normalized data 
            poll_id = polls.next_id() 

            data["choices"] = map(lambda x: x.upper(), data["choices"])

            norm_data = {
                "_id" : poll_id,
                "title" : data["title"],
                "user" : {
                    "$ref" : "users", 
                    "$id" : user["_id"]
                }, 
                "meta" : {
                    "no_of_answers" : 0
                },
                "chart_data" : {

                }, 
                "bot_flags" : {
                    "is_locked" : False
                },
                "created_at" : created_at
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
            
            data["answer"] = data["answer"].upper()

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
                "answer" : data["answer"], 
                "answered_at" : datetime.now()
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

            # increase no. of votes in poll
            polls.coll.update_one(
                { "_id" : poll_id }, 
                { "$inc" : { "meta.no_of_answers" : 1 }},
                session=session
            )

            return inserted_id 

    def get_answered_polls(user): 
        answered_polls = answers.coll.find({
            "user.$id" : user["_id"]
        })  
        answered_polls = list(map(lambda x: x["poll"].id, answered_polls))  
        return answered_polls

    def browse_polls(
        query, sort = "recent", filter_ = "all", cursor = -1, **kwargs
    ): 
        answered_polls = [] 

        base_projection = {
            "_id" : 1, 
            "title" : 1, 
            "user" : 1, 
            "meta" : 1, 
            "chart_data" : 1, 
            "created_at" : 1
        }

        user = kwargs.get("user", None)

        if user is not None:
            answered_polls = Voting.get_answered_polls(user)
        

        sort_order = None 

        if sort == "recent": 
            sort_order = {
                "created_at" : -1
            }    

        elif sort == "oldest": 
            sort_order = {
                "created_at" : 1
            }
   
        else: 
            raise Exception("Unknown sort mode [" + sort + "]")

        cursor_cond = None 

        if sort == "recent" or sort == "most_voted": 
            cursor_cond = "$lt" 
            
            if cursor == -1: 
                cursor = float('infinity')

        elif sort == "oldest" or sort == "least_voted": 
            cursor_cond = "$gt"

        matcher =  None 

        if filter_ == "answered": 
            matcher = {
                "$and" : [
                    { "_id" : { cursor_cond : cursor } },
                    { "_id" : { "$in" : answered_polls }}
                ],
                "title" : { "$regex" : query }
            }

        elif filter_ == "unanswered": 
            matcher  = {
                "$and" : [
                    { "_id" : { cursor_cond : cursor } },
                    { "_id" : { "$nin" : answered_polls }}
                ],
                "title" : { "$regex" : query }
            }

        else:
            matcher = {}

        agg = [
            {
                "$match" : matcher
            },
            {
                "$lookup" : {
                    "from" : "users", 
                    "localField" : "user.$id", 
                    "foreignField" : "_id",
                    "as" : "user"
                }
            }, 
            {
                "$project" : {
                    **base_projection, 
                    "user": { "$arrayElemAt": [ "$user", 0 ] }
                }
            }, 
            { 
                "$sort" : sort_order
            }, 
            {
                "$limit" : 10
            }
        ]

        if filter_ == "all": 
            poll_count = polls.coll.count_documents(matcher)
            sorted_polls = \
                list(polls.coll.aggregate(agg))

            meta = {}
            if len(sorted_polls) > 0: 
                meta["next_cursor"] = sorted_polls[-1]["_id"] 
            meta["count"] = poll_count

            return {
                "data" : sorted_polls, 
                "meta" : meta
            }


        elif filter_ == "answered": 
            # query = {
            #     "title" : { "$regex" : query },
            #     "poll.$id" : { "$in" : answered_polls }
            # }

            poll_count = polls.coll.count_documents(matcher)
            sorted_polls = \
                list(polls.coll.aggregate(agg))

            
            meta = {}
            if len(sorted_polls) > 0: 
                meta["next_cursor"] = sorted_polls[-1]["_id"] 
            meta["count"] = poll_count
            
            return {
                "data" : sorted_polls, 
                "meta" : meta
            }


        elif filter_ == "unanswered": 
            # query = {
            #     "title" : { "$regex" : query },
            #     "poll.$id" : { "$nin" : answered_polls }
            # }

            poll_count = polls.coll.count_documents(matcher)
            sorted_polls = \
                list(polls.coll.aggregate(agg))
            
            meta = {}
            if len(sorted_polls) > 0: 
                meta["next_cursor"] = sorted_polls[-1]["_id"] 
            meta["count"] = poll_count

            return {
                "data" : sorted_polls, 
                "meta" : meta
            }

        else: 
            raise Exception("Unknown filter mode [" + filter_ + "].")  

        return sorted_polls

    def get_poll_choices(poll_id, limit = 8, cursor = -1): 

        choice_count = \
            choices.coll.count_documents({ "poll.$id" : poll_id })

        choice_list = choices.coll.find({
            "poll.$id" : poll_id,
            "_id" : { "$gt" : cursor }
        })
        
        choice_list = list(choice_list.limit(limit))
        
        meta = {}
        if len(choice_list) > 0: 
            meta["next_cursor"] = choice_list[-1]["_id"]
        meta["total"] = choice_count

        return {
            "data" : choice_list, 
            "meta" : meta
        }

    def find_in_choices(poll_id, q, limit = 8, cursor = -1): 
        search = {
            "poll.$id" : poll_id, 
            "answer" : { "$regex" : q }, 
            "_id" : { "$gt" : cursor }
        }

        choice_count = \
            choices.coll.count_documents(search)

        choice_list = list(choices.coll.find(search).limit(limit)) 

        meta = {} 
        if len(choice_list) > 0: 
            meta["next_cursor"] = choice_list[-1]["_id"]
        meta["total"] = choice_count

        return {
            "data" : choice_list, 
            "meta" : meta
        }

    def get_poll_summary(poll_id): 
        summary = answers.coll.aggregate([
            {
                "$match" : {
                    "poll.$id" : poll_id
                }
            },
            { 
                "$group" : {
                    "_id" : "$answer", 
                    "count" : { "$sum" : 1 }
                }
            },
            { "$limit" : 10 }
        ])

        return summary

    def clear_polls():
        polls.coll.drop()  

    def does_poll_exist(poll_id): 
        return polls.exists(poll_id)

    def get_random_poll(user): 
        answered_polls = Voting.get_answered_polls(user)
        
        result = list(polls.coll.aggregate([
            { "$match" : { "_id" : { "$nin" : answered_polls }}}, 
            { "$sample" : { "size" : 1 } }
        ]))[0]

        return dumps(result)

    def denormalized_answer_list(matcher, submatch = {}):
        base_projection = {
            "_id" : 1,
            "answer" : 1, 
            "answered_at" : 1, 
            "user" : 1, 
            "poll" : 1
        }

        answers_list = list(answers.coll.aggregate([
            {
                "$match" : matcher
            }, 
            {
                "$sort" : {
                    "answered_at" : -1
                }
            }, 
            {
                "$lookup" : {
                    "from" : "users", 
                    "localField" : "user.$id", 
                    "foreignField" : "_id", 
                    "as" : "user"
                }
            }, 
            {
                "$lookup" : {
                    "from" : "polls", 
                    "localField" : "poll.$id", 
                    "foreignField" : "_id", 
                    "as" : "poll"
                }
            },
            {
                "$project" : {
                    **base_projection, 
                    "user": { "$arrayElemAt": [ "$user", 0 ] }, 
                    "poll": { "$arrayElemAt": [ "$poll", 0 ] }, 
                }
            }, 
            {
                "$match" : submatch
            },
            {
                "$limit" : 10
            }
        ]))

        return answers_list

    def denormalized_poll_list(matcher):
        base_projection = {
            "_id" : 1,
            "title" : 1, 
            "user" : 1, 
            "meta" : 1, 
            "chart_data" : 1, 
            "created_at" : 1
        }

        polls_list = list(polls.coll.aggregate([
            {
                "$match" : matcher
            }, 
            {
                "$lookup" : {
                    "from" : "users", 
                    "localField" : "user.$id", 
                    "foreignField" : "_id", 
                    "as" : "user"
                }
            }, 
            {
                "$project" : {
                    **base_projection, 
                    "user": { "$arrayElemAt": [ "$user", 0 ] }
                }
            }, 
            {
                "$sort" : {
                    "answered_at" : -1
                }
            }, 
            {
                "$limit" : 10
            }
        ]))

        return polls_list
    
    def get_polls_by_user(user, query, cursor):
        matcher = {
            "user.$id" : user["_id"], 
            "_id" : { "$gt" : cursor },
            "title" : { "$regex" : query }
        }

        poll_count = polls.coll.count_documents(matcher)

        polls_list = Voting.denormalized_poll_list(matcher)


        next_cursor = None
        if len(polls_list) > 0: 
            next_cursor = polls_list[-1]["_id"] 

        return {
            "meta" : {
                "total" : poll_count, 
                "next_cursor" : next_cursor
            },
            "data" : polls_list
        }

    def get_answers_by_user(user, query, cursor): 
        matcher = {
            "user.$id" : user["_id"], 
            "_id" : { "$gt" : cursor }
        }

        submatch = {
            "$or" : [
               { "answer" : { "$regex" : re.compile(query, re.IGNORECASE) } }, 
               { "poll.title" : { "$regex" : re.compile(query, re.IGNORECASE) } }, 
            ]
        }

        answers_count = answers.coll.count_documents(matcher)

        answers_list = Voting.denormalized_answer_list(matcher, submatch)

        next_cursor = None
        if len(answers_list) > 0: 
            next_cursor = answers_list[-1]["_id"] 

        return {
            "meta" : {
                "total" : answers_count, 
                "next_cursor" : next_cursor
            },
            "data" : answers_list
        }


    def recent_answers(): 
        answers_list = Voting.denormalized_answer_list({})
        return answers_list 

    def count_polls(): 
        return polls.coll.count_documents({}) 

    def count_answerees(): 
        return users.coll.count_documents({})

    def count_average_answers():
        total_answers = answers.coll.count_documents({}) 
        total_polls = polls.coll.count_documents({})
        average = total_answers // total_polls
        return average