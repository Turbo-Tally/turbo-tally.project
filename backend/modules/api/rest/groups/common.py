
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

from modules.common.locations import regions, provinces

common_blueprint  = \
    Blueprint('common', __name__, template_folder="./templates")


#
# GET /regions 
# 
@common_blueprint.route("/regions", methods=["GET"]) 
def common__regions(): 
    return regions

# 
# GET /region/<region_id>/provinces 
#   
@common_blueprint.route("/region/<region_id>/provinces", methods=["GET"]) 
def common__region_provinces(region_id): 
    # validate data 
    data = {} 
    data["region_id"] = region_id 

    schema = {
        "region_id" : formats["region"]
    }

    v = Validator(schema)
    v.validate(data) 

    if v.errors != {}: 
        return {
            "status" : "REGION_DOES_NOT_EXIST"
        } 

    # get province of regions 
    province_list = \
        list(filter(lambda e: e["region"] == region_id, provinces))

    return province_list
