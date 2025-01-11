"""Code Citation: ZMQ socket derived from  suggestion_service.py code by Seth Mackovjak @seth08"""
from constants import *
import zmq
from time import sleep
from datetime import datetime

# wishlist list
wishlist = []

class WishListService:
    def __init__(self, socket=None) -> None:
        print("Server initializing... ", end="")
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind(socket or ConnectionEnum.SERVER_SOCKET3.value)
        self.listener()

    def listener(self) -> None:
        """
        Listener method continuously waiting for request.
        """

        print("Done.")
        while True:
            # recieve object at socket and print
            recv_data = self.socket.recv_pyobj()
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S%z'), f"Request recieved: {recv_data}", end="\n\t")
            
            # add object and return updated wishlist
            try:
                self.add_wishlist(recv_data)
                self.socket.send_pyobj(wishlist)
            except Exception as e:
                print(e)
            else:
                print(f"Response Sent: {wishlist}")

            sleep(0.1)

    def add_wishlist(self, data=None):
        """Adds a list containing hike info to the wishlist list."""
        if type(data) not in (type(None), list):
            print("Error - invalid parameter")
            return data
        # if request is read only, don't add
        if data == [None, None, None]:
            return wishlist
        wishlist.append(data)

if __name__ == '__main__':

    WishListService()
