#
# :: fetch_exchange_rates.py
# Get exchange rates daily.
# 
from dotenv import load_dotenv 
from datetime import date 
from time import sleep
import requests

load_dotenv(".env")

REFRESH_INTERVAL = 60

from scans.repositories.exchange_rates import exchange_rates
from scans.core.logger import Logger

Logger.clear("scripts/fetch_exchange_rates")

def main(): 
    # make endpoint
    endpoint = \
        "https://v6.exchangerate-api.com/v6" + \
        "/4dcf98427175f9a64b50e47b/latest/USD"

    # continuously poll endpoint for new date 
    while True: 
        # get date today 
        today = date.today() 
        today_str = today.strftime("%Y/%m/%d") 
        
        # check if date exists 
        record_exists = exchange_rates.exists(today_str)

        # if no records exists yet, register new rates 
        if not record_exists: 
            # log new fetch
            Logger.log(
                "scripts/fetch_exchange_rates",
                f"> New date detected ({today_str}), " +
                "fetching exchange rates."
            )

            # get exchange rates data
            Logger.log(
                "scripts/fetch_exchange_rates", 
                "\t@ Fetching exchange rates data."
            ) 
            data = requests.get(endpoint)
            result = data.json() 

            # create data to insert
            data = {
                "date" : today_str, 
                "data" : result
            }

            # insert data to database
            Logger.log(
                "scripts/fetch_exchange_rates",
                "\t@ Inserting data to database."
            ) 
            exchange_rates.create(data)

    # apply refresh interval 
    sleep(REFRESH_INTERVAL)


if __name__ == "__main__": 
    main()