
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
        "poll_id" : { "type" : "string" }, 
        "answer"  : formats["poll_choice"]  
    }

    data = request.json 
    data["poll_id"] = poll_id

    v = Validator(schema) 
    v.validate(data) 

    if v.errors != {}: 
        return {
            "status" : "VALIDATION_ERROR" 
        }

    # check if poll has already been answered 
    user = request.app["user"]
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
    data = request.args 
    
    schema = {
        "q" : { "type" : "string" }, 
        "sort" : {
            "type" : "string",
            "allowed" : [ 
                "recent", 
                "oldest",
                "most_voted", 
                "most_viewed", 
                "least_viewed",
                "least_voted"
            ]
        },
        "filter" : {
            "type" : "string", 
            "allowed" : [ "all", "unanswered", "answered" ]
        }
    }

    polls = Voting.browse_polls(data["q"], data["sort"], data["filter"]) 

    polls = dumps(polls)

    return polls

#
# POST /voting/polls/<poll_id>/info 
# 
@voting_blueprint.route("/polls/<poll_id>/info", methods=["GET"])
def voting__poll_info(poll_id): 
    # validate data 
    data = {}
    data["poll_id"] = poll_id

    schema = {
        "poll_id" : { "type" : "string" }
    } 

    v = Validator(schema)
    v.validate(data) 

    # check if poll does not exist 
    if not polls.coll.find_one({ "_id" : poll_id }): 
        return {
            "status" : "POLL_DOES_NOT_EXIST"
        }


    # get info about polls 
    poll = polls.read(poll_id) 

    return dumps(poll)

#
# POST /voting/polls/<poll_id>/choices
# 
@voting_blueprint.route("/polls/<poll_id>/choices", methods=["GET"])
def voting__poll_choices(poll_id): 
     # validate data 
    data = {}
    data["poll_id"] = poll_id

    schema = {
        "poll_id" : { "type" : "string" }
    } 

    v = Validator(schema)
    v.validate(data) 

    # check if poll does not exist 
    if not polls.coll.find_one({ "_id" : poll_id }): 
        return {
            "status" : "POLL_DOES_NOT_EXIST"
        }

    # get info about polls 
    poll = polls.read(poll_id)
    choices = poll["info"]["choices"]   

    return dumps(choices)

#
# GET /voting/polls/<poll_id>/find-choices 
# 
@voting_blueprint.route("/polls/<poll_id>/find-choices", methods=["GET"]) 
def voting__poll_find_choices(poll_id):
    # data 
    data = dict(request.args) 
    data["poll_id"] = poll_id 

    schema = {
        "poll_id" : { "type" : "string" }, 
        "q" : { "type" : "string" }
    } 

    v = Validator(schema)
    v.validate(data)
 
    # find in choices 
    poll = polls.coll.find_one({ "_id" : poll_id })
    choices = poll["info"]["choices"]

    choice_list = [] 

    for choice in choices: 
        if re.search(data["q"], choice) is not None:
            choice_list.append(choice) 
        else:   
            continue

    return choice_list


#
# POST /voting/polls/<poll_id>/summary 
# 
@voting_blueprint.route("/polls/<poll_id>/summary", methods=["GET"]) 
def voting__poll_summary(): 
    pass 
 
