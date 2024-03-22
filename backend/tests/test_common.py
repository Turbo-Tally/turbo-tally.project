import os
import requests
from dotenv import load_dotenv  

from .init_tests import BASE_URL

class TestCommon: 

    def test_can_ping_server(self):
        response = requests.get(f"{BASE_URL}/ping") 
        assert response.text == "PONG"