#
# :: verif_codes.py 
# Repository for `verif_codes` collection. 
# 
from modules.core.repository import Repository 

class VerifCodes(Repository): 
    def __init__(self): 
        
        self.collection_name = "verif_codes" 
        self.main_key        = "handle"

        Repository.__init__(self)

verif_codes = VerifCodes()