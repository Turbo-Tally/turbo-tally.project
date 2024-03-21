#
# :: rest_api.py
# Create the REST APi of the backend.
#

from flask import Flask, render_template, request
from flask_cors import CORS
from modules.core.logging import Logger
from datetime import datetime
from cerberus import Validator  

from modules.main.auth import auth
from modules.common.formats import formats, extend_format, require_all
from modules.common.schemas import schemas

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

        # create normalized registration data
        norm_data = {
            "info" : {
                "birthdate" : data["birthdate"],  
                "gender" : data["gender"], 
                "region" : data["region"],
                "province" : data["province"],
                "mobile_no" : data["mobile_no"]
            }, 
            "auth" : {
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

        return {
            "status" : "REGISTERED", 
            "data" : norm_data
        } 

    #
    # POST /auth/log-in 
    #  
    @app.route("/auth/log-in", methods=["POST"])
    def auth__log_in(): 
        pass 

    #
    # POST /auth/forgot-password
    # 
    @app.route("/auth/forgot-password", methods=["POST"])
    def auth__forgot_password(): 
        pass 

    #
    # POST /auth/logout 
    # 
    @app.route("/auth/logout", methods=["POST"])
    def auth__logout(): 
        pass 
    
    #
    # GET /auth/user 
    # 
    @app.route("/auth/user", methods=["GET"])
    def auth__user(): 
        pass

    return app

   