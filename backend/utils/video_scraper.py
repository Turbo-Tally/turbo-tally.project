
"""
    Extracts the following small set information about a video_id: 
    1) Video/Stream Title 
    2) Channel
""" 

class VideoScraper: 
    def __init__(self, video_id): 
        self.video_id = video_id 
        self.title = None 
        self.channel = None 
        self.extract_data() 

    def extract_data(self):  
        from bs4 import BeautifulSoup
        import requests
        
        html = \
            requests\
                .get(f'https://www.youtube.com/watch?v={self.video_id}')\
                .text

        soup = BeautifulSoup(html, features="html.parser")

        # extract title 
        title = soup.find('meta', { 'name': 'title' })["content"]
        
        # extract channel
        channel = soup.find("link", { 'itemprop': 'name'})["content"]

        self.title = title 
        self.channel = channel

if __name__ == "__main__":
    scraper = VideoScraper("wLZe70e_aPo") 
    print(scraper.__dict__)
     