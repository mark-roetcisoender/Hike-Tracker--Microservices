"""Code Citation: ZMQ socket derived from  suggestion_service.py code by Seth Mackovjak @seth08"""
from constants import *
import zmq
from time import sleep
from datetime import datetime


class ConversionClient:
    def __init__(self, socket=None):

        self.socket_addr = socket or ConnectionEnum.CLIENT_SOCKET1.value
        
        self.context = zmq.Context()
        self.context.setsockopt(zmq.RCVTIMEO, 1000) 
        self.context.setsockopt(zmq.LINGER, 500)

    def convert_obj(self, unit_list=None) -> list:
        """Try to send list with Imperial measurements through the socket & listen for response"""

        converted_units = None
        try:
            socket = self.context.socket(zmq.REQ)
            socket.connect(self.socket_addr)
            socket.send_pyobj(unit_list)
            converted_units = socket.recv_pyobj()
            socket.disconnect(self.socket_addr)
        except Exception as e:
            print(f"Communication error: {e}.")
        print(type(converted_units), converted_units)

        return converted_units

