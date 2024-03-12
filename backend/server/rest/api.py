from flask import render_template, request
from datetime import date
from flask_socketio import rooms
from time import time

from scans.DAL import dal
from scans.TaskManager import task_manager
from scans.VideoInfo import VideoInfo


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
    # GET /mock-client
    # 
    @app.route("/test-client")
    def test_client(): 
        return render_template("test-client.html")
 
    #
    # GET /task-manager/state 
    # 
    @app.route("/task-manager/state") 
    def task_manager_state(): 
        return task_manager.state

    #
    # GET /task-manager/threads 
    # 
    @app.route("/task-manager/threads") 
    def task_manager_threads(): 
        return {
            "tasks" : list(task_manager.threads["tasks"].keys()),
            "streams" : list(task_manager.threads["streams"].keys()), 
            "analyzers" : list(task_manager.threads["analyzers"].keys()),
            "collectors" : list(task_manager.threads["collectors"].keys())
        }
    
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
        task_id = task_manager.preprocess(stream_ids) 
        return {
            "task_id" : task_id, 
            "stream_ids" : stream_ids, 
            "status" : "PREPROCESSING"
        }

    #
    # GET /tasks/{task_id}/info 
    # 
    @app.route("/tasks/<task_id>/info")
    def task_info(task_id):
        task = dal.models["tasks"].read(task_id) 
        del task["_id"]
        return task 

    #
    # GET /streams/{stream_id}/info 
    # 
    @app.route("/streams/<stream_id>/info")
    def stream_info(stream_id): 
        # get video info 
        info = VideoInfo(stream_id)

        # create initial record for the video 
        if not dal.models["streams"].exists(stream_id):
            dal.models["streams"].create({
                "stream_id" : info.video_id, 
                "channel_id" : info.channel_id, 
                "fetch_state" : {
                    "lf_video_time" : "00:00", 
                    "lf_video_id" : None, 
                    "total_messages_fetched" : 0
                }, 
                "reports" : {

                }, 
                "created_at" : time(), 
                "updated_at" : None
            })

        # retrieve stream from database 
        stream = dal.models["streams"].read(stream_id) 

        # attach details to stream 
        stream["_meta"] = {
            "title" : info.title, 
            "channel" : info.channel, 
        }

        # remove object id from stream details
        del stream["_id"] 

        return stream


    #
    # GET /task-manager/rooms 
    # 
    @app.route("/task-manager/rooms") 
    def task_manager_rooms(): 
        return task_manager.rooms

    #
    # GET /messages/count  
    # 
    @app.route("/messages/count")
    def messages_count():
        return str(dal.models["messages"]\
            .context\
            .count_documents({ "message_id" : { "$ne" : 1}}))
        