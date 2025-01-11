"""Code Citation: ZMQ socket derived from  suggestion_service.py code by Seth Mackovjak @seth08"""
from constants import *
import zmq


class HelpClient:
    def __init__(self, socket=None):
        """Set up socket to microservice"""

        self.socket_addr = socket or ConnectionEnum.CLIENT_SOCKET2.value
        self.context = zmq.Context()
        self.context.setsockopt(zmq.RCVTIMEO, 1000)
        self.context.setsockopt(zmq.LINGER, 500)

    def get_text(self, data=None) -> str:
        """Attempts to connect to microservice and sent parameter string. Listens for
        response and returns response to main program"""

        message = None
        try:
            socket = self.context.socket(zmq.REQ)
            socket.connect(self.socket_addr)
            socket.send_string(data)
            message = socket.recv_string()
            socket.disconnect(self.socket_addr)
        except Exception as e:
            print(f"Communication error: {e}.")
        # print to console
        print(message)

        return message

