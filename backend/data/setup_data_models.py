
# setup data models 
from scans.DAL import dal 
from scans.DataModel import DataModel 

dal.models["tasks"]            = DataModel(dal, "tasks", "task_id") 
dal.models["messages"]         = DataModel(dal, "messages", "message_id") 
dal.models["exchange_rates"]   = DataModel(dal, "exchange_rates", "date") 
dal.models["streams"]          = DataModel(dal, "streams", "stream_id")