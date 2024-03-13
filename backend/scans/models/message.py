#
# :: message.py 
# Message model.
# 
from scans.core.model import Model

class Message(Model): 
    def __init__(self): 
        # initialize parent class 
        Model.__init__()