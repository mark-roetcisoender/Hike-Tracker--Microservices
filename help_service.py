"""Code Citation: ZMQ socket derived from  suggestion_service.py code by Seth Mackovjak @seth08"""
from constants import *
import zmq
from time import sleep
from datetime import datetime

class HelpService:
    def __init__(self, socket=None) -> None:
        print("Server initializing... ", end="")
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind(socket or ConnectionEnum.SERVER_SOCKET2.value)
        self.listener()

    def listener(self) -> None:
        """
        Listener method continuously waiting for request.
        """

        print("Done.")
        while True:
            # recieve object at socket and print
            recv_data = self.socket.recv_string()
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S%z'), f"Request recieved: {recv_data}", end="\n\t")
            # determine what text to send back and send it
            try:
                send_data = self.find_text(recv_data)
                self.socket.send_string(send_data)
            except Exception as e:
                print(e)
            else:
                print(f"Response Sent: {send_data}")

            sleep(0.1)

    def find_text(self, data=None) -> str:
        """Returns a help message based on input string parameter"""
        if data == "":
            print("Error - invalid parameter")
            return data
        response = ""
        # data = int(data)
        if data == "add":
            response = "How do I add a hike? Navigate to Add Hike. You'll have the option to either manually enter a hike, or select a hike from a list of hikes already entered. Once the addition is complete, you'll see a success message."
        if data == 'view':
            response = "Where can I see my hikes? Navigate to Hike Log. You'll be able to see a list of hikes that you've logged, along with their stats."
        if data == 'find':
            response = "How can I have a hike suggested to me? Navigate to Find Hike. If you have at least one logged hike, your average hike distance will be used to suggest a new hike for you. "
        if data == 'stats':
            response = "Where can I see my cumulative stats? Navigate to Stats. You'll be able to see a list of stats compileds from your logged hikes, including the overall number of hikes, the total distance traveled, the total elevation gain, the average distance per hike, and the average elevation gained per hike. "
        if data == 'wl':
            response = "How do I track hikes I want to complete? Navigate to Wishlist. You'll be able to add to and see a list of hikes that you've saved for future reference."
        return response

if __name__ == '__main__':

    HelpService()
