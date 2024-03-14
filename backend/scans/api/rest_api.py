#
# :: rest_api.py
# Create the REST APi of the backend.
#

from flask import Flask, render_template
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

    #
    # GET /channel/add/<channel_id>
    # 
    @app.route("/admin/<admin_api_key>/channels/add/<channel_id>") 
    def channel_add(admin_api_key, channel_id):
        # check if admin API key is valid
        if admin_api_key != os.getenv("ADMIN_API_KEY"): 
            return "UNAUTHORIZED"

        # add channel 
        from scans.services.admin import Admin 
        return Admin.register_channel(channel_id)

    # return app instance 
    return app
