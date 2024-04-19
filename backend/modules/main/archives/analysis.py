#
# :: analyzer.py 
# Contains the Analyzer class for analysis related operations.
#

from modules.repositories.answers import answers 
from modules.repositories.users import users 
from modules.repositories.polls import polls 
from modules.repositories.choices import choices 

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

    def denormalized_answer_list(poll_id, aside_query = []):

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

        
    def analyze_poll(poll_id):
        # get choices of polls 
        choice_list  = \
            list(map(lambda e: e["answer"], choices.coll.find({ "poll.$id" : poll_id})))

        # get answers of polls
        answers_per_day = list(Analyzer.denormalized_answer_list(poll_id, [
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

        #
        # BAR CHARTS AND FUNNEL CHARTS
        # 

        # get answers by choice 
        answers_by_choice = list(Analyzer.denormalized_answer_list(poll_id, [
            {
                "$group" : {
                    "_id" : "$answer", 
                    "answer_count" : { "$sum" : 1 }
                }
            }
        ]))

        # get answers by age 
        answers_by_age = list(Analyzer.denormalized_answer_list(poll_id, [
            {
                "$group" : {
                    "_id" : "$user__age", 
                    "answer_count" : { "$sum" : 1 }
                }
            }
        ]))

        answers_by_age.sort(key=lambda e: e["_id"])

        # 
        # STACKED CHARTS
        # 

        # get answers by age in stacked format
        stacked_by_age = list(Analyzer.denormalized_answer_list(poll_id, [
            {
                "$group" : {
                    "_id" : {
                        "age" : "$user__age", 
                        "answer" : "$answer"
                    }, 
                    "answer_count" : { "$sum" : 1 }
                }
            }
        ]))

        stacked_by_age.sort(key=lambda e: 
            (e["_id"]["age"], e["_id"]["answer"])
        )

        # get answers by gender in stacked format
        stacked_by_gender = list(Analyzer.denormalized_answer_list(poll_id, [
            {
                "$group" : {
                    "_id" : {
                        "gender" : "$user.info.gender", 
                        "answer" : "$answer"
                    }, 
                    "answer_count" : { "$sum" : 1 }
                }
            }
        ]))

        stacked_by_gender.sort(key=lambda e: 
            (e["_id"]["gender"], e["_id"]["answer"])
        )

        # get answers by gender in stacked format
        stacked_by_region = list(Analyzer.denormalized_answer_list(poll_id, [
            {
                "$group" : {
                    "_id" : {
                        "region" : "$user.info.region", 
                        "answer" : "$answer"
                    }, 
                    "answer_count" : { "$sum" : 1 }
                }
            }
        ]))

        stacked_by_region.sort(key=lambda e: 
            (e["_id"]["region"], e["_id"]["answer"])
        )

        #
        # BY REGION 
        #
        
        # get total answers by region
        answers_by_region = list(Analyzer.denormalized_answer_list(poll_id, [
            {
                "$group" : {
                    "_id" : "$user.info.region", 
                    "answer_count" : { "$sum" :  1 }
                }
            }
        ]))

        answers_by_region.sort(key=lambda e: e["_id"])

        #
        # BY GENDER 
        #
        
        # get total answers by province
        answers_by_gender = list(Analyzer.denormalized_answer_list(poll_id, [
            {
                "$group" : {
                    "_id" : "$user.info.gender", 
                    "answer_count" : { "$sum" :  1 }
                }
            }
        ]))

        answers_by_gender.sort(key=lambda e: e["_id"])

        #
        # BY PROVINCE 
        #
        
        # get total answers by province
        answers_by_province = list(Analyzer.denormalized_answer_list(poll_id, [
            {
                "$group" : {
                    "_id" : "$user.info.province", 
                    "answer_count" : { "$sum" :  1 }
                }
            }
        ]))

        answers_by_province.sort(key=lambda e: e["_id"])

        # get stacked answers by province 
        stacked_by_province = list(Analyzer.denormalized_answer_list(poll_id, [
            {
                "$group" : {
                    "_id" : {
                        "province" : "$user.info.province", 
                        "answer" : "$answer"
                    }, 
                    "answer_count" : { "$sum" : 1 }
                }
            }
        ]))

        stacked_by_province.QD        # get choices of polls 
        choice_list  = \
            list(
                map(lambda e: e["answer"], 
                choices.coll.find({ "poll.$id" : poll_id}))
            )

        # get answers by day 
        answers_per_day = list(Analyzer.denormalized_answer_list(poll_id, [
            {
                "$match" : {
                    "user.info.province" : province_id
                }
            },
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

        # get answers by choice
        answers_by_choice = list(Analyzer.denormalized_answer_list(poll_id, [
           {
                "$match" : {
                    "user.info.province" : province_id
                }
            },
            {
                "$group" : {
                    "_id" : "$answer", 
                    "answer_count" : { "$sum" : 1 }
                }
            }
        ])) 

        answers_by_choice.sort(key=lambda e: e["_id"])

        # get answers stacked by age
        answers_by_age = list(Analyzer.denormalized_answer_list(poll_id, [
            {
                "$match" : {
                    "user.info.province" : province_id
                }
            },   
            {
                "$group" : {
                    "_id" : {
                        "age" : "$user__age", 
                        "answer" : "$answer"
                    }, 
                    "answer_count" : { "$sum" : 1 }
                }
            }
        ]))

        answers_by_age.sort(key=lambda e: (e["_id"]["age"], e["_id"]["answer"]))

        # get answers stacked by gender
        answers_by_gender = list(Analyzer.denormalized_answer_list(poll_id, [
            {
                "$match" : {
                    "user.info.province" : province_id
                }
            },   
            {
                "$group" : {
                    "_id" : {
                        "gender" : "$user.info.gender", 
                        "answer" : "$answer"
                    }, 
                    "answer_count" : { "$sum" : 1 }
                }
            }
        ]))

        answers_by_gender.sort(key=lambda e: (e["_id"]["gender"], e["_id"]["answer"]))


        return { 
            "choice_list" : choice_list, 
            "per_day_answers" : answers_per_day, 
            "answers_by_choice" : answers_by_choice, 
            "stacked_by_age" : answers_by_age, 
            "stacked_by_gender" : answers_by_gender
        }