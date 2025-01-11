"""Code Citation: ZMQ socket derived from  suggestion_service.py code by Seth Mackovjak @seth08"""
from constants import *
import zmq
from time import sleep
from datetime import datetime


class WishListClient:
    def __init__(self, socket=None):

        self.socket_addr = socket or ConnectionEnum.CLIENT_SOCKET3.value
        
        self.context = zmq.Context()
        self.context.setsockopt(zmq.RCVTIMEO, 1000)
        self.context.setsockopt(zmq.LINGER, 500)

    def add_hike(self, hike=None):
        """Attempt to send hike to be added through socket and listen for updated
        wishlist log to be sent back"""

        try:
            socket = self.context.socket(zmq.REQ)
            socket.connect(self.socket_addr)
            socket.send_pyobj(hike)
            wishlist = socket.recv_pyobj()
            print(wishlist)
            socket.disconnect(self.socket_addr)
        except Exception as e:
            print(f"Communication error: {e}.")
            return -1

        return wishlist
