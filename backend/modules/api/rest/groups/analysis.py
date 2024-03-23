
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

#
# GET /analysis/polls/<poll_id> 
# 
@analysis_blueprint.route("/polls/<poll_id>", methods=["GET"]) 
def analysis__poll(poll_id):
    # validate arguments 
    poll_id = int(poll_id) 
    data = {}
    data["poll_id"] = poll_id 

    schema = {
        "poll_id" : { "type" : "integer" }
    }

    v = Validator(schema)
    v.validate(data) 

    # check if poll does not exist
    if not Voting.does_poll_exist(data["poll_id"]):
        return { 
            "status" : "POLL_DOES_NOT_EXIST"
        }

    # get results for poll 
    results = Analyzer.analyze_poll(poll_id)    

    return dumps(results)


# GET /analysis/polls/<poll_id>/province/<province_id>
# 
@analysis_blueprint.route("/polls/<poll_id>/province/<province_id>", methods=["GET"]) 
def analysis__poll_province(poll_id, province_id):
    # validate arguments 
    poll_id = int(poll_id) 
    province_id = province_id

    data = {}
    data["poll_id"] = poll_id 
    data["province_id"] = province_id

    schema = {
        "poll_id" : { "type" : "integer" }, 
        "province_id" : formats["province"] 
    }

    v = Validator(schema)
    v.validate(data) 

    # check if poll does not exist
    if not Voting.does_poll_exist(data["poll_id"]):
        return { 
            "status" : "POLL_DOES_NOT_EXIST"
        }

    # get results for poll 
    results = Analyzer.analyze_poll_province(
        data["poll_id"], 
        data["province_id"]
    )    

    return dumps(results)