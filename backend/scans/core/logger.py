#
# :: logger.py 
# Logger helper.
#
# Usage: 
#   Logger.log("default", "Hello, there! - from script.py")
# 
from datetime import datetime
import os

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

    def clear_all(name): 
        os.rmdir("./logs/")

    def log(name, data, **kwargs): 
        if name not in Logger.disabled_logs:
            path = f"./logs/{name}.log"
            os.makedirs(os.path.dirname(path), exist_ok=True)
            f = open(path, "a")
            f.write(
                str(datetime.now().strftime("%m\%d\%Y %H:%M:%S")) + 
                " | " + 
                data + 
                (kwargs.get("end") or "\n")
            )
            f.close()



