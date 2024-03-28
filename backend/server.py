from modules.core.logging import Logger

#
# Clear server logs. 
# 
Logger.clear_all("api")

#
# Pre-initialization...
# 
import utils.preloader

#
# Load API server. 
# 
from modules.api.api_server import APIServer 

api_server = APIServer()
api_server.init()
api_server.run() 