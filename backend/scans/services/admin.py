#
# Administrator Service 
# 
from scans.repositories.channels import channels 
from scans.core.cache import redis
import json

class Admin: 
    def register_channel(channel_id):
        # check if channel exists 
        from chat_downloader.sites import YouTubeChatDownloader
        
        try:
            downloader = YouTubeChatDownloader() 
            downloader.get_user_videos(channel_id)
        except: 
            return "CHANNEL_INACCESSIBLE"

        # check if channel is already registered 
        from scans.repositories.channels import channels 
        if channels.exists(channel_id): 
            return "CHANNEL_ALREADY_REGISTERED"

        # create channel data
        data = { 
            "channel_id"  : channel_id, 
            "stream_list" : {}
        }

        # insert to database 
        insert_id = channels.coll.insert_one(data).inserted_id 

        # publish event 
        redis.publish("channel_monitoring", json.dumps({
            "event" : "channel_added", 
            "data" : {
                "channel_id" : channel_id
            }
        }))

        # remove object id from data
        del data["_id"]

        return {
            "status" : "ADDED",
            "data" : data
        }