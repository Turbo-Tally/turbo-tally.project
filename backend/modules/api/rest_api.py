#
# :: rest_api.py
# Create the REST APi of the backend.
#

from flask import Flask, render_template, request, make_response
from flask_cors import CORS
from modules.core.logging import Logger
from datetime import datetime
from cerberus import Validator  
from bson.objectid import ObjectId

import uuid

from modules.main.auth import auth

from modules.common.formats \
    import formats, extend_format, require_all, datetime_format
from modules.common.schemas import schemas
from modules.common.password_generation import random_password

from modules.repositories.verif_codes import verif_codes
from modules.repositories.users import users
from modules.repositories.sessions import sessions

import os

def create_rest_api(): 
    # setup paths 
    STATIC_FOLDER    = os.path.abspath("./static") 
    TEMPLATES_FOLDER = os.path.abspath("./templates")

    # create flask app 
    app = Flask(
        __name__,
        static_url_path  = "", 
        static_folder    = STATIC_FOLDER,
        template_folder  = TEMPLATES_FOLDER
    ) 

    # allow cross origin request
    CORS(
        app,
        supports_credentials = True, 
        resource = {
            r"/*" : {
                "origins" : "*"
            }
        }
    )

    @app.before_request
    def hook():
        request.app = {}
        session_id = request.cookies.get("SESSION_ID")
        if session_id is not None: 
            request.app["user"] = auth.get_session_user(session_id)

    ################
    # SETUP ROUTES #
    ################

    #
    # GET / 
    # 
    @app.route("/") 
    def index(): 
        return render_template("index.html")

    #
    # GET /ping
    #
    @app.route("/ping")
    def ping():
        return "PONG" 

    ############################
    # AUTHENTICATION ENDPOINTS # 
    ############################

    #
    # POST /auth/sign-up 
    # 
    @app.route("/auth/sign-up", methods=["POST"]) 
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
            "created_at" : "2022-01-01", 
            "updated_at" : None
        }

        # add raw password when in development mode 
        if os.getenv("ENV_MODE") == "dev": 
            norm_data["auth"]["password"] = data["password"]

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
        if not auth.check_verif_code(data["email"], data["email_code"]): 
            return {
                "status" : "INVALID_EMAIL_CODE"
            }

        # check if sms verification code is invalid 
        if not auth.check_verif_code(data["mobile_no"], data["sms_code"]): 
            return {
                "status" : "INVALID_SMS_CODE"
            }
        
        auth.clear_verif_code(data["mobile_no"])
        auth.clear_verif_code(data["email"])

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
    @app.route("/auth/generate-verif-code", methods=["GET"])
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
    @app.route("/auth/verify-code", methods=["POST"])
    def auth__verify_code():
        handle = request.args.get("handle")
        code = request.args.get("code") 

        # check if code is correct 
        is_valid = auth.check_verif_code(handle, code)

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
    @app.route("/auth/user/check-if-exists", methods=["GET"])
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
    @app.route("/auth/session-id", methods=["GET"]) 
    def auth__session_id(): 
        res = make_response()
        res.set_cookie("SESSION_ID", value=str(uuid.uuid4()))
        return res

    #
    # POST /auth/log-in 
    #  
    @app.route("/auth/log-in", methods=["POST"])
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
    @app.route("/auth/user", methods=["GET"])
    def auth__user(): 
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
    @app.route("/auth/log-out", methods=["GET"])
    def auth__logout(): 
        user = request.app["user"] 
        auth.clear_session_user(request.cookies.get("SESSION_ID"))
        return {
            "status" : "USER_LOGGED_OUT"
        }
    
    #
    # GET /auth/forgot-password
    # 
    @app.route("/auth/forgot-password", methods=["GET"])
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


    return app

   