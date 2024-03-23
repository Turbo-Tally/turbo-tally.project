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
import os

from modules.main.auth import auth

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
            if auth.is_session_logged_in(session_id):
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
    from .groups.auth import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    ####################
    # VOTING ENDPOINTS #
    #################### 
    from .groups.voting import voting_blueprint 
    app.register_blueprint(voting_blueprint, url_prefix="/voting") 

    ######################
    # ANALYSIS ENDPOINTS #
    ###################### 
    from .groups.analysis import analysis_blueprint 
    app.register_blueprint(analysis_blueprint, url_prefix="/analysis") 

    ############## 
    # EXPOSE APP #
    ##############
    return app 