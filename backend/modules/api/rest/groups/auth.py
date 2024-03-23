
from flask import Flask, render_template, request, make_response, Blueprint
from flask_cors import CORS
from modules.core.logging import Logger
from datetime import datetime
from cerberus import Validator  
from bson.objectid import ObjectId

import uuid
import os

from modules.main.auth import auth

from modules.common.formats \
    import formats, extend_format, require_all, datetime_format, is_province_allowed
from modules.common.schemas import schemas
from modules.common.password_generation import random_password

from modules.repositories.verif_codes import verif_codes
from modules.repositories.users import users

############################
# AUTHENTICATION ENDPOINTS # 
############################

auth_blueprint = \
    Blueprint('auth', __name__, template_folder="./templates")

#
# POST /auth/sign-up 
# 
@auth_blueprint.route("/sign-up", methods=["POST"]) 
def auth__sign_up():
    data = request.json

    # define schema for validation
    schema = schemas["registration_input"]

    # validator 
    v = Validator(schema) 
    v.validate(data) 

    if v.errors != {}: 
        return {
            "status" : "VALIDATION_ERROR", 
            "errors" : v.errors
        }

    # create normalized registration data
    norm_data = {
        "info" : {
            "birthdate" : 
                datetime.strptime(data["birthdate"], datetime_format),  
            "gender" : data["gender"], 
            "region" : data["region"],
            "province" : data["province"],
            "mobile_no" : data["mobile_no"]
        }, 
        "auth" : {
            "username" : data["username"],
            "email" : data["email"], 
            "password_hash" : auth.hash(data["password"]),
            "is_admin" : False, 
            "is_bot" : False
        },
        "created_at" : datetime.now().strftime(datetime_format), 
        "updated_at" : None
    }

    # add raw password when in development mode 
    if os.getenv("ENV_MODE") == "dev": 
        norm_data["auth"]["password"] = data["password"]

    # check if province is allowed 
    if not is_province_allowed(data["region"], data["province"]): 
        return {
            "status" : "PROVINCE_NOT_ALLOWED"
        }

    # check if username already exists 
    if auth.check_if_user_already_exists_by(
        "auth.username", data["username"]
    ): 
        return {
            "status" : "USERNAME_ALREADY_EXISTS"
        }
    
    # check if email already exists 
    if auth.check_if_user_already_exists_by(
        "auth.email", data["email"]
    ): 
        return {
            "status" : "EMAIL_ALREADY_EXISTS"
        }

    # check if phone number already exists 
    if auth.check_if_user_already_exists_by(
        "info.mobile_no", data["mobile_no"]
    ): 
        return {
            "status" : "MOBILE_NO_ALREADY_EXISTS"
        }

    # check if email verification codes is invalid 
    if not auth.check_verif_code(
        "email-verif", data["email"], data["email_code"]
    ): 
        return {
            "status" : "INVALID_EMAIL_CODE"
        }

    # check if sms verification code is invalid 
    if not auth.check_verif_code(
        "mobile-verif", data["mobile_no"], data["sms_code"]
    ): 
        return {
            "status" : "INVALID_SMS_CODE"
        }
    
    auth.clear_verif_code("mobile-verif", data["mobile_no"])
    auth.clear_verif_code("email-verif", data["email"])

    # register user in the database 
    auth.create_user(norm_data)

    # remove _id from norm_data 
    del norm_data["_id"]

    return {
        "status" : "REGISTERED", 
        "data" : norm_data
    } 

#
# GET /auth/generate-code
#  
@auth_blueprint.route("/generate-verif-code", methods=["GET"])
def auth__generate_code():
    type_  = request.args.get("type") 
    handle = request.args.get("handle")
    code, expiration_time = auth.generate_verif_code()

    # generate output data
    out_data =  {
        "status" : "GENERATED", 
        "args" : {
            "type" : type_, 
            "handle" : handle
        }
    }

    # save code to database 
    auth.register_verif_code(type_, handle, code, expiration_time)

    # if in development mode, respond with verif. code
    out_data["code"] = {
        "value" : code, 
        "expiration_time" : expiration_time
    }

    return out_data

#
# POST /auth/verify-code 
# 
@auth_blueprint.route("/verify-code", methods=["POST"])
def auth__verify_code():
    type_ = request.args.get("type")
    handle = request.args.get("handle")
    code = request.args.get("code") 

    # check if code is correct 
    is_valid = auth.check_verif_code(type_, handle, code)

    if not is_valid: 
        return {
            "status" : "INVALID_CODE", 
            "message" : "Code entered was invalid."
        } 
    

    return {
        "status" : "VALID_CODE", 
        "message" : "Code entered was valid."
    }

#
# GET /auth/check-if-exists
# 
@auth_blueprint.route("/user/check-if-exists", methods=["GET"])
def auth__user__check_if_exists():
    schema =  {
        "by" : { 
            "type" : "string", 
            "allowed" : [
                "auth.email", 
                "auth.username",
                "info.mobile_no"
            ] 
        }, 
        "value" : {
            "type" : "string"
        }
    }

    v = Validator(schema) 
    v.validate(request.args) 

    if v.errors != {}: 
        return {
            "status" : "VALIDATION_ERROR", 
            "errors" : v.errors
        }

    by = request.args.get("by") 
    value = request.args.get("value")

    user_exists = \
        auth.check_if_user_already_exists_by(by, value) 

    if user_exists: 
        return {
            "status" : "USER_ALREADY_EXISTS"
        }
    else: 
        return {
            "status" : "USER_DOES_NOT_EXIST"
        }

#
# GET /auth/session-id 
#  
@auth_blueprint.route("/session-id", methods=["GET"]) 
def auth__session_id(): 
    res = make_response()
    res.set_cookie("SESSION_ID", value=str(uuid.uuid4()))
    return res

#
# POST /auth/log-in 
#  
@auth_blueprint.route("/log-in", methods=["POST"])
def auth__log_in(): 
    session_id = request.cookies.get("SESSION_ID")
    
    email = request.json.get("email") 
    password = request.json.get("password")

    if not auth.check_if_user_already_exists_by("auth.email", email): 
        return {
            "status" : "EMAIL_DOES_NOT_EXIST"
        }

    user = auth.find_user_by_email(email)

    input_password = auth.hash(request.json.get("password")) 
    target_password = user["auth"]["password_hash"]

    if input_password != target_password: 
        return {
            "status" : "INVALID_PASSWORD"
        }

    auth.set_session_user(session_id, str(user["_id"]))

    return {
        "status" : "LOGGED_IN",
        "user_id" : str(user["_id"])
    }

#
# GET /auth/user 
# 
@auth_blueprint.route("/user", methods=["GET"])
def auth__user(): 
    if "user" not in request.app: 
        return {
            "status" : "USER_NOT_LOGGED_IN"
        }

    user = request.app["user"]

    if user is None: 
        return {
            "status" : "USER_NOT_LOGGED_IN"
        }

    user["_id"] = str(user["_id"])
    del user["auth"]["password"]

    return {
        "status" : "USER_LOGGED_IN",
        "data" : user
    }

#
# GET /auth/logout 
# 
@auth_blueprint.route("/log-out", methods=["GET"])
def auth__logout(): 
    user = request.app["user"] 
    auth.clear_session_user(request.cookies.get("SESSION_ID"))
    return {
        "status" : "USER_LOGGED_OUT"
    }

#
# GET /auth/forgot-password
# 
@auth_blueprint.route("/forgot-password", methods=["GET"])
def auth__forgot_password(): 
    email = request.args.get("email")
    
    if not auth.check_if_user_already_exists_by("auth.email", email): 
        return {
            "status" : "EMAIL_DOES_NOT_EXIST"
        }
    
    user = users.coll.find_one({ "auth.email" : email })
    user_id = user["_id"]

    new_password = random_password(32)

    # output data 
    out_data = {
        "status" : "TEMPORARY_PASSWORD_SENT"
    }

    # update password in database 
    users.update(user_id, {
        "auth.password" : new_password, 
        "auth.password_hash" : auth.hash(new_password)
    })

    if os.getenv("ENV_MODE") == "dev": 
        out_data["temporary_password"] = new_password

    return out_data

#
# POST /auth/update-info
# 
@auth_blueprint.route("/update-info", methods=["POST"]) 
def auth__update_info(): 
    data = request.json

    # define schema for validation
    schema = schemas["info_update_input"]

    # validator 
    v = Validator(schema) 
    v.validate(data)  

    if v.errors != {}: 
        return {
            "status" : "VALIDATION_ERROR", 
            "errors" : v.errors
        }

    # normalize bithdate 
    if "birthdate" in data:
        data["birthdate"] = \
            datetime.strptime(data["birthdate"], datetime_format)

    if "province" in data: 
        region = None 
        if "region" in data: 
            if not is_province_allowed(data["region"], data["province"]): 
                return {
                    "status" : "PROVINCE_NOT_ALLOWED"
                } 
        else:
            user = request.app["user"]
            info = user["info"]
            if not is_province_allowed(info["region"], data["province"]): 
                return {
                    "status" : "PROVINCE_NOT_ALLOWED"
                } 

    # update user info 
    auth.update_user_info(request.app["user"]["_id"], data)

    return {
        "status" : "INFO_UPDATED"
    }


#
# POST /auth/change-email
# 
@auth_blueprint.route("/change-email", methods=["POST"]) 
def auth__change_email(): 
    data = request.json
    user = request.app["user"]

    # define schema for validation
    schema = {
        "email" : formats["email"],
        "code"  : formats["verif_code"]
    }

    # validator 
    v = Validator(schema) 
    v.validate(data)  

    # check if verification code is correct
    if not auth.check_verif_code(
        "email-change", data["email"], data["code"]
    ):
        return {
            "status" : "INVALID_CODE"
        }

    # clear verification code 
    auth.clear_verif_code("email-change", data["email"])

    # change email of user 
    users.coll.update_one(
        { "_id" : user["_id"]}, 
        {
            "$set" : {
                "auth.email" : data["email"]
            }
        }
    )

    return {
        "status" : "EMAIL_CHANGED"
    }



# POST /auth/change-password
# 
@auth_blueprint.route("/change-password", methods=["POST"]) 
def auth__change_password(): 
    data = request.json
    user = request.app["user"]

    # define schema for validation
    schema = {
        "current_password" : { "type" : "string" }, 
        "new_password" : formats["password"]
    }

    # validator 
    v = Validator(schema) 
    v.validate(data)  

    print("Cookies :", request.cookies)

    # check if current password matches
    current_password_hash = user["auth"]["password_hash"] 
    if auth.hash(data["current_password"]) != current_password_hash: 
        return {
            "status" : "INVALID_CURRENT_PASSWORD"
        }

    # change password 
    users.coll.update_one(
        { "_id" : user["_id"] }, 
        { 
            "$set" : { 
                "auth.password" : data["new_password"], 
                "auth.password_hash" : auth.hash(data["new_password"])
            }
        }
    )

    return {
        "status" : "PASSWORD_CHANGED"
    }