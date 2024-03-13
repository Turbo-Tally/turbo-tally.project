#
# :: logger.py 
# Logger helper.
#
# Usage: 
#   Logger.log("default", "Hello, there! - from script.py")
# 
from datetime import datetime

class Logger:
    disabled_logs = set()

    def disable(name):
        Logger.disabled_logs.add(name) 

    def enable(name): 
        if name in Logger.disabled_logs:
            Logger.disabled_logs.remove(name)

    def clear(name):
        f = open(f"./logs/{name}.log", "w")
        f.close()

    def log(name, data, **kwargs): 
        if name not in Logger.disabled_logs:
            f = open(f"./logs/{name}.log", "a")
            f.write(
                str(datetime.now().strftime("%m\%d\%Y %H:%M:%S")) + 
                " | " + 
                data + 
                (kwargs.get("end") or "\n")
            )
            f.close()



