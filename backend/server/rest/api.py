from flask import render_template, request
from datetime import date
from scans.DAL import dal
from scans.TaskManager import task_manager

def make_rest_api(app): 
    
    #
    # GET / 
    # 
    @app.route("/") 
    def index(): 
        return render_template("index.html")

    #
    # GET /rates
    # 
    @app.route("/rates") 
    def rates(): 
        today = date.today() 
        today_str = today.strftime("%Y/%m/%d")
        rates = dal.models["exchange_rates"].read(today_str) 
        del rates["_id"]
        return rates

    #
    # GET /task-manager/state 
    # 
    @app.route("/task-manager/state") 
    def task_manager_state(): 
        return task_manager.state
    
    #
    # GET /ping
    # 
    @app.route("/ping")
    def ping():
        return "PONG"


    #
    # GET /tasks/new 
    # 
    @app.route("/tasks/new") 
    def tasks_new(): 
        stream_ids = request.args.get("stream_ids").split(",")
        task_id, video_infos = task_manager.preprocess(stream_ids) 
        return {
            "task_id" : task_id, 
            "stream_ids" : stream_ids, 
            "streams" : video_infos,
            "status" : "PREPROCESSING"
        }
