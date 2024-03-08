from bs4 import BeautifulSoup
import requests
from .DataWrapper import DataWrapper
from time import time

class VideoInfo: 
    def __init__(self, video_id): 
        self.video_id = video_id 
        self.title = None 
        self.channel = None 

        video_in_db = DataWrapper.of("streams").read(self.video_id)

        if video_in_db is not None:
            self.title = video_in_db["meta"]["title"] 
            self.channel = video_in_db["meta"]["channel"]
        else:
            self.extract_data()  
            DataWrapper.of("streams").create({
                "stream_id": self.video_id, 
                "meta" : {
                    "title" : self.title, 
                    "channel" : self.channel 
                },
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

    def extract_data(self):  
        html = \
            requests\
                .get(f'https://www.youtube.com/watch?v={self.video_id}')\
                .text

        soup = BeautifulSoup(html, features="html.parser")

        # extract title 
        title = soup.find('meta', { 'name': 'title' })["content"]
        
        # extract channel
        channel = soup.find("link", { 'itemprop': 'name'})["content"]

        self.title = title or "<unknown>"
        self.channel = channel or "<unknown>"

