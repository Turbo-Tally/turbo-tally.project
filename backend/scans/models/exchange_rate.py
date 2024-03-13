#
# :: exchange_rate.py 
# ExchangeRate model.
# 
from scans.core.model import Model

class ExchangeRate(Model): 
    def __init__(self): 
        # initialize parent class 
        Model.__init__()