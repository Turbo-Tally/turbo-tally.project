
class Room: 
    def __init__(self, room_id, socket_io): 
        self.room_id = room_id 
        self.socket_io = socket_io
    
    def run(self):
        def run_in_background(): 
            self.background_runner()

        self.socket_io.start_background_task(run_in_background)

    def background_runner(self):
        """
            To implement via child class. 
        """ 
        pass 