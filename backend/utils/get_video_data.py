#
# get_video_data.py 
# :: A short script to get the data of a YouTube video.
# 

from chat_downloader.sites import YouTubeChatDownloader
import json

from .video_map import VIDEO_MAP

VIDEO_ID = VIDEO_MAP["Enzo Recto : Sample 1"]

downloader = YouTubeChatDownloader()

data = downloader.get_video_data(VIDEO_ID) 

print(json.dumps(data, indent=2))
