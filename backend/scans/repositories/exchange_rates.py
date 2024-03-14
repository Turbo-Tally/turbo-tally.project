#
# :: exchange_rates.py 
# Repository for `exchange_rates` collection. 
#  
from scans.core.repository import Repository 

class ExchangeRates(Repository): 
    def __init__(self): 
        
        self.collection_name = "exchange_rates" 
        self.main_key        = "date"

        Repository.__init__(self)

exchange_rates = ExchangeRates()