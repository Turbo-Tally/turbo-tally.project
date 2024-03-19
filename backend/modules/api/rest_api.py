#
# :: rest_api.py
# Create the REST APi of the backend.
#

from flask import Flask, render_template
from flask_cors import CORS
from modules.core.logging import Logger
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


    return app

   