from dotenv import load_dotenv 

#
# Load environment file (.env) 
#
load_dotenv(".env")

#
# Load API server. 
# 
from scans.api.api_server import APIServer 

api_server = APIServer()
api_server.init()
api_server.run() 