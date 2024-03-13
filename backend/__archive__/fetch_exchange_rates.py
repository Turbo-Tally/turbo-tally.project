from time import time, sleep
from datetime import date
from dotenv import load_dotenv 
import requests

load_dotenv(".env")

INTERVAL = 1 

import data.setup_data_models 
from scans.DAL import dal 

endpoint = \
    "https://v6.exchangerate-api.com/v6/4dcf98427175f9a64b50e47b/latest/USD"

while True:
    today = date.today()
    today_str = today.strftime("%Y/%m/%d")

    exists = dal.models["exchange_rates"].exists(today_str)

    if not exists: 
        print("> New date detected, fetching exchange rates.")
        data = requests.get(endpoint) 
        result = data.json() 

        insert_data = {
            "date" : today_str,
            "data" : result
        }

        dal.models["exchange_rates"].create(insert_data)

   
    sleep(INTERVAL)