from dotenv import load_dotenv 
from modules.core.logger import Logger

#
# Clear server logs. 
# 
Logger.clear_all("api")

#
# Load environment file (.env) 
#
load_dotenv(".env")

#
# Pre-initialization.
# 
import utils.pre_initializer

#
# Load API server. 
# 
from modules.api.api_server import APIServer 

api_server = APIServer()
api_server.init()
api_server.run() 