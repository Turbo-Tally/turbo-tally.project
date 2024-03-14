#
# :: monitor_channels.py
# Monitor channels and get livesream data.
# 

from dotenv import load_dotenv 
from threading import Thread
from time import time, sleep
import os
import json
import requests
from chat_downloader.sites import YouTubeChatDownloader
from chat_downloader import ChatDownloader

load_dotenv(".env")

from scans.core.logger import Logger

from scans.repositories.channels import channels
from scans.repositories.streams import streams
from scans.repositories.messages import messages

Logger.clear("scripts/monitor_channels")

# records of currently monitored channels 
active_channels = {} 

# threads 
threads = {
    "main" : {}, 
    "monitors" : {},
    "back_monitors" : {}
} 

# check if no. of channels match database
def check_sync_channels(): 
    if len(active_channels.keys()) != channels.count_all():
        Logger.log("scripts/monitor_channels", "> (SYNC) Should fix channels.")
        fix_channels() 
    else: 
        Logger.log("scripts/monitor_channels", "> (SYNC) No need fix channels.")


# fix channels by finding unsynced channels
def fix_channels():
    active_ids = list(active_channels.keys())
    to_add_channels = \
        channels.coll.find({ "channel_id" : { "$nin" : active_ids }}) 
    
    Logger.log("scripts/monitor_channels", "@ Fixing channels for:")
    for to_add_channel in to_add_channels: 
        Logger.log(
            "scripts/monitor_channels", 
            "\t" + to_add_channel["channel_id"]
        )  
        spawn_channel_monitor(to_add_channel["channel_id"])
        active_channels[to_add_channel["channel_id"]] = time()

    Logger.log("scripts/monitor_channels", "@ SYNCED")

# receive events via pub-sub
def listen_for_events():
    Logger.log(
        "scripts/monitor_channels", 
        "> (EVENT_LISTENER) Started event listener..."
    )
    from scans.core.cache import redis 
    p = redis.pubsub() 

    def handle_event(message):
        data = json.loads(message["data"])
        process_event(data["event"], data["data"])

    p.subscribe(**{
        "channel_monitoring" : handle_event
    })

    threads["main"]["event_listener_sub"] = \
        p.run_in_thread(sleep_time=0.01)

# process event
def process_event(event, data): 
    Logger.log(
        "scripts/monitor_channels",
        f"(EVENT_LISTENER) Received event `{event}`."
    )

    if event == "channel_added": 
        spawn_channel_monitor()

# sync channels from time to time 
def sync_channels_periodically():
    SYNC_REFRESH_RATE = float(os.getenv("SYNC_REFRESH_RATE"))
    while True: 
        check_sync_channels()
        sleep(SYNC_REFRESH_RATE)

# spawn channel monitor 
def spawn_channel_monitor(channel_id):
    monitor_log_file = f"scripts/monitors/{channel_id}"

    def monitor_function(): 
        
        Logger.clear(monitor_log_file)
        Logger.log(monitor_log_file, f"> Monitoring {channel_id}")

        downloader = YouTubeChatDownloader()
        
        MONITOR_REFRESH_RATE = float(os.getenv("MONITOR_REFRESH_RATE"))

        # # back monitor videos 
        # threads["back_monitors"][channel_id] = \
        #     Thread(target=back_monitor, args=(channel_id,))
        # threads["back_monitors"][channel_id].start()

        # process latest live video
        while True: 
            streams = downloader.get_user_videos(channel_id, video_type="live")
            
            latest_video = get_first_video(channel_id)
            Logger.log(
                monitor_log_file, 
                f"\t:: Fetched latest video id {latest_video['video_id']} " + 
                f"-> {latest_video['title']}"
            )

            video_id = latest_video["video_id"]
            video_type = latest_video["video_type"]

            if video_type == "LIVE": 
                Logger.log(
                    monitor_log_file,
                    "\t\t@ Is live video, monitoring."
                )
                monitor_video(channel_id, video_id)
            else: 
                Logger.log(
                    monitor_log_file,
                    "\t\t@ Is not live video, skipping."
                )

            sleep(MONITOR_REFRESH_RATE)

    if channel_id not in active_channels and \
       channel_id not in threads["monitors"]: 
        threads["monitors"][channel_id] = \
            Thread(target=monitor_function)
        threads["monitors"][channel_id].start()

def monitor_video(channel_id, video_id): 
    monitor_log_file = f"scripts/monitors/{channel_id}"

    def collect_messages():     
        Logger.log(monitor_log_file, f"> Collecting messages for {video_id}.")
        
        while True:
            # create downloader
            downloader = ChatDownloader() 
            url = f"https://www.youtube.com/watch?v={video_id}"
            messages = downloader.get_chat(url) 

            # store information about stream    
            if not streams.exists(video_id):
                streams.blank(video_id, channel_id)

            # collect messages
            for message in messages: 
                if message["message_type"] in ["paid_sticker", "paid_item"]: 
                    store_message(channel_id, stream_id, message)


            # handle situation where message stream has ended 
            first_video = get_first_video(channel_id) 

            if first_video["video_id"] == video_id and \
                first_video["video_type"] == "DEFAULT": 
               break
            elif first_video["video_type"] == "LIVE": 
               continue

    collect_messages()

# get first video of a channel
def get_first_video(channel_id): 
    downloader = YouTubeChatDownloader()
    videos = downloader.get_user_videos(channel_id, video_type="live") 
    for video in videos: 
        return video 

def store_message(channel_id, stream_id, message):
    monitor_log_file = f"scripts/monitors/{channel_id}"

    if not messages.exists(message["message_id"]):
        Loggger.log(monitor_log_file, "> Stored 1 superchat.")
        messages.create({
            "message_id" : message["message_id"], 
            "channel_id" : channel_id, 
            "stream_id"  : stream_id, 
            "message_type" : message["message_type"], 
            "author" : {
                "author_id" : message["author"]["id"], 
                "name" : message["author"]["name"]
            }
        })

# # process older messages (back monitor channel)
# def back_monitor(channel_id):
#     # create two downloader
#     ytcd_a = YouTubeChatDownloader() 
#     ytcd_b = YouTubeChatDownloader() 

#     # create thread function for monitor_a 
#     def run_monitor_a(): 
#         stream_list = ytcd_a.get_user_videos(channel_id, video_type="live")

#         for stream in stream_list: 
#             store_stream(channel_id, stream)
 
#     # create thread function for monitor_b 
#     def run_monitor_b(): 
#         MONITOR_B_WAITING_TIME = \
#             float(os.getenv("MONITOR_B_WAITING_TIME")) 

#         while True: 
#             stream_list = ytcd_b.get_user_videos(channel_id, video_type="live")

#             for stream in stream_list:
#                 stream_id = stream["video_id"]

#                 if channels.streamExistsIn(stream_id, channel_id):
#                     break 
                
#                 store_stream(channel_id, stream)

#             sleep(MONITOR_B_WAITING_TIME)

#     # create threads for monitor_a and monitor_b 
#     threads["monitors"][f"A:{channel_id}"] = \
#         Thread(target=run_monitor_a) 
#     threads["monitors"][f"B:{channel_id}"] = \
#         Thread(target=run_monitor_b) 
    
#     # start monitor threads
#     threads["monitors"][f"A:{channel_id}"].start() 
#     threads["monitors"][f"B:{channel_id}"].start()


# # store stream 
# def store_stream(channel_id, stream):
#     # get video id 
#     video_id = stream['video_id']

#     # register stream in channel 
#     channels\
#         .coll\
#         .update_one(
#             { "channel_id" : channel_id }, 
#             { "$set" : { "stream_list." + video_id : True }}
#         )

#     # create stream 
#     streams.blank(video_id, channel_id)

def main():

    # create syncing thread
    threads["main"]["channel_syncing"] = \
        Thread(target=sync_channels_periodically)
    threads["main"]["channel_syncing"].start()
    
    # create event listener thread 
    threads["main"]["event_listener"] = \
        Thread(target=listen_for_events) 
    threads["main"]["event_listener"].start()

if __name__ == "__main__":
    main()