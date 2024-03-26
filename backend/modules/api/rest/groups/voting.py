
from flask import Flask, render_template, request, make_response, Blueprint
from flask_cors import CORS
from modules.core.logging import Logger
from datetime import datetime
from cerberus import Validator  
from bson.objectid import ObjectId
from bson.json_util import dumps

import re
import uuid
import os

from modules.main.auth import auth

from modules.common.formats \
    import formats, extend_format, require_all, datetime_format, is_province_allowed
from modules.common.schemas import schemas
from modules.common.password_generation import random_password

from modules.repositories.verif_codes import verif_codes
from modules.repositories.users import users
from modules.repositories.polls import polls
from modules.repositories.answers import answers

from modules.main.voting import Voting

############################
# AUTHENTICATION ENDPOINTS # 
############################

voting_blueprint = \
    Blueprint('voting_blueprint', __name__, template_folder="./templates")

#
# POST /voting/polls/create
# 
@voting_blueprint.route("/polls/create", methods=["POST"]) 
def voting__create_poll(): 
    # validate inputs
    schema = {
        "title"   :  formats["poll_title"], 
        "choices" :  { 
            "type" : "list", 
            "schema" : formats["poll_choice"]
        } 
    } 
    
    require_all(schema)

    data = request.json

    v = Validator(schema)
    v.validate(data)

    if v.errors != {}: 
        return {
            "status" : "VALIDATION_ERROR",
            "errors" : v.errors
        }

    # check if choices contain duplicates 
    choices_set = set() 

    for choice in data["choices"]: 
        if choice in choices_set: 
            return {
                "status" : "DUPLICATE_CHOICES"
            }
        choices_set.add(choice)

    # create poll 
    user = request.app["user"]

    insert_id = Voting.create_poll(user, data)

    return {
        "status" : "POLL_CREATED",
        "poll_id" : str(insert_id)
    }

#
# POST /voting/polls/answer
#  
@voting_blueprint.route("/polls/<poll_id>/answer", methods=["POST"]) 
def voting__answer_poll(poll_id):
    # validate data 
    schema = {
        "poll_id" : { "type" : "integer" }, 
        "answer"  : formats["poll_choice"] , 
    }

    data = request.json 
    data["poll_id"] = int(poll_id)

    v = Validator(schema) 
    v.validate(data) 

    if v.errors != {}: 
        return {
            "status" : "VALIDATION_ERROR", 
            "errors" : v.errors
        }

    # check if poll exists 
    if polls.coll.find_one({ "_id" : data["poll_id"] }) is None:
        return {
            "status" : "POLL_DOES_NOT_EXIST"
        }
 
    # check if poll has already been answered 
    user = request.app["user"]
    if user is None: 
        return { 
            "status" : "NOT_LOGGED_IN"
        }
    
    if answers.coll.find_one({ 
        "user.$id" : user["_id"],
        "poll.$id" : data["poll_id"]
    }): 
        return {
            "status" : "ALREADY_ANSWERED"
        }

    # answer poll 
    user = request.app["user"]
    Voting.answer_poll(user, data)

    return {
        "status" : "ANSWER_SUBMITTED"
    }

#
# POST /voting/polls/browse
#  
@voting_blueprint.route("/polls/browse", methods=["GET"])
def voting__browse_polls(): 
    # validate schema 
    data = dict(request.args) 
    data["cursor"] = int(data.get("cursor", -1))
    
    schema = {
        "q" : { "type" : "string" }, 
        "sort" : {
            "type" : "string",
            "allowed" : [ 
                "recent", 
                "oldest",
                "most_voted"
                "least_voted"
            ]
        },
        "filter" : {
            "type" : "string", 
            "allowed" : [ "all", "unanswered", "answered" ]
        }
    }

    polls = Voting.browse_polls(
        data["q"], 
        data["sort"], 
        data["filter"],
        data["cursor"], 
        user=request.app["user"]
    ) 

    polls = dumps(polls)

    return polls

#
# POST /voting/polls/<poll_id>/info 
# 
@voting_blueprint.route("/polls/<poll_id>/info", methods=["GET"])
def voting__poll_info(poll_id): 
    # validate data 
    data = {}
    data["poll_id"] = int(poll_id)

    schema = {
        "poll_id" : { "type" : "integer" }
    } 

    v = Validator(schema)
    v.validate(data) 

    # check if poll does not exist 
    if not polls.coll.find_one({ "_id" : data["poll_id"] }): 
        return {
            "status" : "POLL_DOES_NOT_EXIST"
        }

    # get info about polls 
    poll = polls.read(data["poll_id"]) 

    return dumps(poll)

#
# POST /voting/polls/<poll_id>/choices
# 
@voting_blueprint.route("/polls/<poll_id>/choices", methods=["GET"])
def voting__poll_choices(poll_id): 
     # validate data 
    data = dict(request.args) 
    data["poll_id"] = int(poll_id)
    data["cursor"] = int(data.get("cursor", -1))

    schema = {
        "poll_id" : { "type" : "integer" },
        "cursor" : { "type" : "integer" }
    } 

    v = Validator(schema)
    v.validate(data) 

    if v.errors != {}: 
        return {
            "status" : "VALIDATION_ERROR", 
            "errors" : v.errors
        }

    # check if poll exists
    if not Voting.does_poll_exist(data["poll_id"]): 
        return {
            "status" : "POLL_DOES_NOT_EXIST"
        }

    # check if poll does not exist 
    if not polls.coll.find_one({ "_id" : data["poll_id"] }): 
        return {
            "status" : "POLL_DOES_NOT_EXIST"
        }

    # get info about polls 
    choice_list = Voting.get_poll_choices(data["poll_id"], 8, data["cursor"]) 

    return dumps(choice_list)

#
# GET /voting/polls/<poll_id>/find-choices 
# 
@voting_blueprint.route("/polls/<poll_id>/find-choices", methods=["GET"]) 
def voting__poll_find_choices(poll_id):
    # data 
    data = dict(request.args) 
    data["poll_id"] = int(poll_id) 
    data["cursor"] = int(data.get("cursor", -1))

    schema = {
        "poll_id" : { "type" : "string" }, 
        "q" : { "type" : "string" }, 
        "cursor" : { "type" : "integer"}
    } 

    v = Validator(schema)
    v.validate(data)

    # check if poll exists
    if not Voting.does_poll_exist(data["poll_id"]): 
        return {
            "status" : "POLL_DOES_NOT_EXIST"
        }
 
    # find in choices 
    choice_list = Voting.find_in_choices(
        data["poll_id"], 
        data["q"], 
        8, 
        data["cursor"]
    )

    return dumps(choice_list)


#
# POST /voting/polls/<poll_id>/summary 
# 
@voting_blueprint.route("/polls/<poll_id>/summary", methods=["GET"]) 
def voting__poll_summary(poll_id): 
    # request arguments 
    poll_id = int(poll_id) 

    # get poll summary 
    summary = Voting.get_poll_summary(poll_id)

    return dumps(summary)


#
# GET /voting/random-poll 
# 
@voting_blueprint.route("/random-poll", methods=["GET"]) 
def voting__random_poll():
    if "user" not in request.app: 
        return {
            "status" : "NOT_LOGGED_IN"
        }

    user = request.app["user"] 

    # get random poll_id for user 
    return Voting.get_random_poll(user)

#
# GET /voting/polls/by-user
# 
@voting_blueprint.route("/polls/by-user", methods=["GET"])
def voting__polls_by_user(): 
    # validate schema 
    data = dict(request.args)
    data["user"] = int(data["user"])
    data["cursor"] = int(data.get("cursor", -1))

    schema = {
        "user" : { "type" : "integer" },
        "q" : { "type" : "string" }, 
        "cursor" : { "type" : "integer" }
    }   

    v = Validator(schema)
    v.validate(data)

    # get user record 
    user = users.read(data["user"])

    if user is None: 
        return { 
            "status" : "USER_NOT_FOUND"
        }

    # get polls by user 
    polls_list = Voting.get_polls_by_user(
        user, 
        data["q"],
        data["cursor"]
    ) 

    return dumps(polls_list)


#
# GET /voting/answers/by-user
# 
@voting_blueprint.route("/answers/by-user", methods=["GET"])
def voting__answers_by_user(): 
    # validate schema 
    data = dict(request.args)
    data["user"] = int(data["user"])
    data["cursor"] = int(data.get("cursor", -1))

    schema = {
        "user" : { "type" : "integer" },
        "q" : { "type" : "string" }, 
        "cursor" : { "type" : "integer" }
    }   

    v = Validator(schema)
    v.validate(data)

    # get user record 
    user = users.read(data["user"])

    if user is None: 
        return { 
            "status" : "USER_NOT_FOUND"
        }

    # get polls by user 
    answers_list = Voting.get_answers_by_user(
        user, 
        data["q"],
        data["cursor"]
    ) 

    return dumps(answers_list)
