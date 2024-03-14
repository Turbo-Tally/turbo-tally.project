#
# get_videos_list.py
# :: Get all videos of a channel.
# 

#
# get_video_data.py 
# :: A short script to get the data of a YouTube video.
# 

from chat_downloader.sites import YouTubeChatDownloader
import json

from .video_map import VIDEO_MAP

downloader = YouTubeChatDownloader()

videos_list =\
    downloader.get_user_videos(
        VIDEO_MAP["Enzo Recto : Sample 1"], 
        video_type="live"
    )

count = 0
for video in videos_list:
    print(count, " -> ", video)
    count += 1