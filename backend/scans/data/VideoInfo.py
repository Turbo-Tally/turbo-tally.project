from bs4 import BeautifulSoup
import requests

class VideoInfo: 
    def __init__(self, video_id): 
        self.video_id = video_id 
        self.title = None 
        self.channel = None 
        self.extract_data() 

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

