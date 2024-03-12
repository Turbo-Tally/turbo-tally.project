from chat_downloader import ChatDownloader
from flask_socketio import emit
from time import time
from datetime import date
from bson.objectid import ObjectId
import uuid
from threading import Thread

from .DAL import dal
from scans.TaskManager import task_manager

class Collector: 
    def __init__(self, stream_id):   
        self.stream_id = stream_id 
        self.flusher_thread = None 
        self.switch = True 
        self.last_message_timestamp = time()
        self.has_flushed = False 
        self.messages = [] 
        self.start_sending = False

    def clear(self): 
        self.switch = False 
        
        thread = task_manager.threads["collectors"][self.stream_id] 
        thread.join() 

        self.flusher_thread.join() 
        self.relayer_thread.join()

        del task_manager.threads["collectors"][self.stream_id] 

    def runner(self, socket_io): 
        print(f"@ Running collector for stream id [{self.stream_id}]...")
        
        stream_room_id = "stream." + self.stream_id

        # socket_io.send("new_event", to=stream_room_id)

        # create downloader object
        downloader = ChatDownloader()

        # create download url 
        url = f"https://www.youtube.com/watch?v={self.stream_id}" 

        # get start time to fetch 
        stream = dal.models["streams"].read(self.stream_id)
        start_time = stream["fetch_state"]["lf_video_time"]
        
        # download url 
        download = downloader.get_chat(
            url, 
            chat_type="live",
            start_time=start_time
        )

        # create flusher thread 
        self.flusher_thread = \
            socket_io.start_background_task(self.flusher, socket_io)

        # create relayer thread 
        self.relayer_thread = \
            socket_io.start_background_task(self.relayer, socket_io)

        for item in download: 
            data = {}

            data["stream_id"] = self.stream_id

            if "message_id" in item: 
                data["message_id"] = item["message_id"] 

            if "message_type" in item: 
                data["message_type"] = item["message_type"]
            
            if "header_secondary_text" in item: 
                data["header_secondary_text"] = item["header_secondary_text"]

            if "message_text" in item:
                data["message_text"] = item["message_text"]
            
            if "author" in item:
                data["author"] = {
                    "id"     : item["author"]["id"], 
                    "name"   : item["author"]["name"],
                    "image"  : item["author"]["images"][2]["url"]
                } 

            if "money" in item: 
                data["money"] = {
                    "amount"   : item["money"]["amount"], 
                    "currency" : item["money"]["symbol"]
                } 


            print(
                f"[Stream {data['stream_id']} : " + 
                f"Received Message] -> "+ 
                f"{data['message_id']}"
            ) 

            # record message in database 
            if not dal.models["messages"].exists(data["message_id"]):
                print(
                    f"\t-> Recording message in" +
                    f" [{data['message_id']}] database."
                )

                stream = dal.models["streams"].read(self.stream_id)
                total_messages_fetched = \
                    stream["fetch_state"]["total_messages_fetched"]

                # create record in messages table 
                self.messages.append(data)

            if self.start_sending: 
                socket_io.emit("new_message", data, to=stream_room_id)

            self.last_message_timestamp = time()


    def flusher(self, socket_io):   
        stream_room_id = "stream." + self.stream_id 

        while True:
            message_count = len(self.messages)
            # dal.models["messages"].context.insert_many(self.messages) dd
            if message_count > 0:
                f = open("out", "a")
                f.write(
                    f"> {str(date.today().strftime('%Y/%m/%d'))} : " +
                    f"[{self.stream_id}] " + 
                    f"Storing {message_count} messages.\n")
                f.close()
                dal.models["messages"].context.insert_many(self.messages)
                socket_io.emit(
                    "recorded_messages", 
                    {
                        "count" : message_count,
                        "stream_id" : self.stream_id
                    }, 
                    to = stream_room_id
                )

            self.messages = []
            socket_io.sleep(3)  

    def relayer(self, socket_io): 
        while not self.start_sending and time() - self.last_message_timestamp > 5: 
            self.start_sending = True

    def get_flush_data(self, socket_io): 
        pass

           