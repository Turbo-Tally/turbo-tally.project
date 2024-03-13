#
# get_video_data.py 
# :: A short script to get the chat data of a YouTube video.
# 

from chat_downloader import ChatDownloader
import json
from datetime import datetime

from .video_map import VIDEO_MAP

VIDEO_ID = VIDEO_MAP["Kapamilya Online Live : Live"]
url = f"https://www.youtube.com/watch?v={VIDEO_ID}" 

downloader = ChatDownloader() 

stream = downloader.get_chat(url) 
 
for message in stream: 
    print(json.dumps(message, indent=2) + ",")