
from flask import Flask, render_template, request, make_response, Blueprint
from flask_cors import CORS
from modules.core.logging import Logger
from datetime import datetime
from cerberus import Validator  
from bson.objectid import ObjectId
from bson.json_util import dumps

import uuid
import os

from modules.main.auth import auth

from modules.common.formats \
    import formats, extend_format, require_all, datetime_format, is_province_allowed
from modules.common.schemas import schemas
from modules.common.password_generation import random_password

from modules.repositories.verif_codes import verif_codes
from modules.repositories.users import users

from modules.main.voting import Voting
from modules.main.analysis import Analyzer

############################
# AUTHENTICATION ENDPOINTS # 
############################

analysis_blueprint = \
    Blueprint('analysis', __name__, template_folder="./templates")

def validate_poll_id(poll_id):
    poll_id = int(poll_id) 
    data = {}
    data["poll_id"] = poll_id 

    schema = {
        "poll_id" : { "type" : "integer" }
    }

    v = Validator(schema)
    v.validate(data) 
    
    return poll_id

#
# GET /analyze/<poll_id>/choices
# 
@analysis_blueprint.route("/<poll_id>/choices", methods=["GET"]) 
def analysis__choices(poll_id):
    # validate arguments 
    poll_id = validate_poll_id(poll_id)

    # check if poll does not exist
    if not Voting.does_poll_exist(poll_id):
        return { 
            "status" : "POLL_DOES_NOT_EXIST"
        }

    # get choices of poll 
    results = Analyzer.choices(poll_id)

    return dumps(results)


#
# GET /analyze/<poll_id>/answers-per-day 
# 
@analysis_blueprint.route("/<poll_id>/answers-per-day", methods=["GET"]) 
def analysis__answers_per_day(poll_id): 
    # validate arguments 
    poll_id = validate_poll_id(poll_id)

    # check if poll does not exist
    if not Voting.does_poll_exist(poll_id):
        return { 
            "status" : "POLL_DOES_NOT_EXIST"
        }

    # get results for poll 
    results = Analyzer.answers_per_day(poll_id)    

    return dumps(results)


#
# GET /analyze/<poll_id>/answers-by-choice
# 
@analysis_blueprint.route("/<poll_id>/answers-by-choice", methods=["GET"]) 
def analysis__answers_by_choice(poll_id): 
    # validate arguments 
    poll_id = validate_poll_id(poll_id)

    # check if poll does not exist
    if not Voting.does_poll_exist(poll_id):
        return { 
            "status" : "POLL_DOES_NOT_EXIST"
        }

    # get results for poll 
    results = Analyzer.answers_by_choice(poll_id)    

    return dumps(results)


#
# GET /analyze/<poll_id>/answers-by/<type_>
# 
@analysis_blueprint.route("/<poll_id>/answers-by/<type_>", methods=["GET"]) 
def analysis__answers_by(poll_id, type_): 
    # validate arguments 
    poll_id = validate_poll_id(poll_id)

    # check if poll does not exist
    if not Voting.does_poll_exist(poll_id):
        return { 
            "status" : "POLL_DOES_NOT_EXIST"
        }

    # get results for poll 
    if type_ == "age": 
        type_ = "$user__age"
    else: 
        type_ = "$user.info." + type_ 
    results = Analyzer.answers_by(poll_id, type_)    

    return dumps(results)


#
# GET /analyze/<poll_id>/stacked-by/<type_>
# 
@analysis_blueprint.route("/<poll_id>/stacked-by/<type_>", methods=["GET"]) 
def analysis__stacked_by(poll_id, type_): 
    # validate arguments 
    poll_id = validate_poll_id(poll_id)

    # check if poll does not exist
    if not Voting.does_poll_exist(poll_id):
        return { 
            "status" : "POLL_DOES_NOT_EXIST"
        }

    # get results for poll 
    if type_ == "age": 
        type_ = "$user__age"
    else: 
        type_ = "$user.info." + type_ 
    results = Analyzer.stacked_by(poll_id, type_)    

    return dumps(results)