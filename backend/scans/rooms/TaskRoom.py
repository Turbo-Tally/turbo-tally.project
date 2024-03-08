from .Room import Room 
from random import randint

class TaskRoom(Room):
    
    def background_runner(self):    
        # while True: 
        #     random_no = randint(1, 100)
        #     print(f"> {self.room_id} : {random_no}")

        #     data = {
        #         "room_id" : self.room_id, 
        #         "random_no" : random_no
        #     }

        #     self.socket_io.emit("new_message", data, to=self.room_id)
        #     self.socket_io.sleep(1) 
        pass