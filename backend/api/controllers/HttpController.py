

class HttpController:
    def ping(): 
        return "PONG"

    def analyze():
        return {
            "status" : "OK", 
            "message" : "task_dispatched", 
            "details" : {
                
            }
        }