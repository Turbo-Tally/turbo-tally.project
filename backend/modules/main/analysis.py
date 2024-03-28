#
# :: analyzer.py 
# Contains the Analyzer class for analysis related operations.
#

from modules.repositories.answers import answers 
from modules.repositories.users import users 
from modules.repositories.polls import polls 
from modules.repositories.choices import choices 

from modules.common.helpers import revalue
from modules.common.locations import region_map, province_map

from datetime import datetime
from bson.json_util import dumps



class Analyzer: 
    compute_age = {
        "$subtract" : [
            { 
                "$subtract" : [ 
                    { "$year" :"$$NOW" },
                    { "$year": "$user.info.birthdate" } 
                ]
            },
            { 
                "$cond" : [
                    { 
                        "$gt" : [ 
                            0, 
                            { 
                                "$subtract": [ 
                                    { "$dayOfYear" : "$$NOW" },
                                    { "$dayOfYear" : "$user.info.birthdate" }
                                ]
                            }
                        ]
                    },
                    1,
                    0
                ]
            }
        ]
    }

    def revalue_generic(context, category, key = "key"): 
        if category == "$user.info.gender": 
            revalue(context, key, {
                "M" : "MALE",
                "F" : "FEMALE"
            })
        elif category == "$user.info.region": 
            revalue(context, key, region_map)
        elif category == "$user.info.province": 
            revalue(context, key, province_map)


    def dal(poll_id, aside_query = []):
        base_projection = {
            "poll" : 1, 
            "user" : 1,
            "answered_at" : 1,
            "answer" : 1, 
            "answer_count" : 1
        }

        base_query = [
            {
                "$match" : {
                    "poll.$id" : poll_id
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
                "$project": { 
                    **base_projection,
                    "user": { "$arrayElemAt": [ "$user", 0 ] }, 
                }
            }, 
            {
                "$project" : {
                    **base_projection,
                    "user__age" : Analyzer.compute_age,
                    "answer_date" : { 
                        "$dateToString" : { 
                            "format" : "%Y-%m-%d", 
                            "date" : "$answered_at" 
                        } 
                    },
                    "answer_time": { 
                        "$dateToString" : { 
                            "format": "%H:%M:%S:%L", 
                            "date": "$answered_at" 
                        } 
                    }
                }
            }
        ]

        expanded_query = base_query + aside_query 

        return answers.coll.aggregate(expanded_query)

    def choices(poll_id):
        choice_list = \
            list(
                map(
                    lambda e: e["answer"], 
                    choices.coll.find({ "poll.$id" : poll_id}))
                )
        return choice_list

    def answers_per_day(poll_id): 
        answers_per_day = list(Analyzer.dal(poll_id, [
            {
                "$group" : {
                    "_id" : "$answer_date", 
                    "answer_count" : { "$sum" : 1 }
                }
            }, 
            {
                "$project" : {
                    "_id" : 1, 
                    "answer_count" : 1
                }
            }
        ]))

        answers_per_day.sort(key=lambda e: e["_id"])

        return answers_per_day

    def answers_by_choice(poll_id): 
        answers_by_choice = list(Analyzer.dal(poll_id, [
            {
                "$group" : {
                    "_id" : "$answer", 
                    "answer_count" : { "$sum" : 1 }
                }
            }
        ]))

        answers_by_choice.sort(key=lambda e: e["_id"])
        
        return answers_by_choice 

    def answers_by(poll_id, category): 
        answers_by = list(Analyzer.dal(poll_id, [
            {
                "$group" : {
                    "_id" : category, 
                    "count" : { "$sum" :  1 }
                }
            },
            {
                "$project" : {
                    "_id" : 0,
                    "key" : "$_id", 
                    "count" : 1
                }
            }
        ]))

        answers_by.sort(key=lambda e: e["key"])

        Analyzer.revalue_generic(answers_by, category)

        return answers_by


    def stacked_by(poll_id, category): 
        stacked_by = list(Analyzer.dal(poll_id, [
            {
                "$group" : {
                    "_id" : {
                        "key" : category, 
                        "answer" : "$answer"
                    }, 
                    "count" : { "$sum" : 1 }
                }
            }, 
            { 
                "$project" : {
                    "_id" : 0,
                    "key"   : "$_id.key", 
                    "subkey" : "$_id.answer", 
                    "count" : 1
                }
            }
        ]))

        stacked_by.sort(key=lambda e: 
            (e["key"], e["subkey"])
        )

        Analyzer.revalue_generic(stacked_by, category)

        return stacked_by

    def paired_map(poll_id, category_a, category_b): 
        paired_map = list(Analyzer.dal(poll_id, [
            {
                "$group" : {
                    "_id" : {
                        "key_a" : category_a, 
                        "key_b" : category_b,
                        "answer" : "$answer"
                    }, 
                    "count" : { "$sum" : 1 }
                }
            }, 
            { 
                "$project" : {
                    "_id" : 0,
                    "key_a"   : "$_id.key_a", 
                    "key_b"   : "$_id.key_b", 
                    "subkey" : "$_id.answer", 
                    "count" : 1
                }
            }
        ]))

        paired_map.sort(key=lambda e: 
            (e["key_a"], e["key_b"], e["subkey"])
        )

        Analyzer.revalue_generic(paired_map, category_a, "key_a")
        Analyzer.revalue_generic(paired_map, category_b, "key_b")

        return paired_map