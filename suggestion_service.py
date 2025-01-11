"""Code Citation: created by Seth Mackovjak (sethm08) for CS361"""
import polars, zmq, numpy
from time import sleep
from datetime import datetime
from random import randint
from constants import *

class SuggestionsClient:
    """ --- To be created/defined in the client program --- """

    def __init__(self, socket=None):
        """
        Desc:   Initialize the SuggestionsClient object.
        Args:
            socket: Socket to be used (e.g. 'tcp://123.456.789:1234')
        """

        self.socket_addr = socket or ConnectionEnum.CLIENT_SOCKET.value
        
        self.context = zmq.Context()
        self.context.setsockopt(zmq.RCVTIMEO, 1000) 
        self.context.setsockopt(zmq.LINGER, 500)

    def request_suggestion(self, trail_length=None) -> dict:
        """
        Desc:   Request method.
        Args:
            trail_length (None/int/float): Approximate trail length requested.
        Return:
            dict{'Name':str, 'Distance':float, 'Elevation Gain':int} or None
        """
        trail_suggestion = None
        if type(trail_length) not in (type(None), int, float):
            try:
                trail_length = float(trail_length)
            except Exception:
                print(f'Error: "{trail_length}" not a numeric value.')
                return None
        try:
            socket = self.context.socket(zmq.REQ)
            socket.connect(self.socket_addr)
            socket.send_pyobj(trail_length)
            trail_suggestion = socket.recv_pyobj()
            socket.disconnect(self.socket_addr)
        except Exception as e:
            print(f"Communication error: {e}.")

        return trail_suggestion

class SuggestionsServer:

    """ --- To be working independently --- """

    def __init__(self, socket=None):
        """
        Desc:   Server to recieve trail length, then select and respond with the
                    chosen trail.
        Args:
            socket (str or None): Socket to be listening on. Defaults to 1234 if
                    left empty.
        """

        print("Server initializing... ", end="")
        self.hike_dataframe = polars.read_excel("./Hike DB.xlsx")
        self.lengths = polars.Series(self.hike_dataframe.get_column('Distance')).to_numpy(writable=True)
        self.n_trails = self.lengths.shape[0]

        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind(socket or ConnectionEnum.SERVER_SOCKET.value)
        self.listener()
        
    def listener(self) -> None:
        """
        Desc:   Listener method continuously waiting for request.
        """

        print("Done.")
        while True:
            trail_length = self.socket.recv_pyobj()
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S%z'), f"Request recieved: {trail_length}", end="\n\t")
            try:
                trail_suggestion = self.findTrail(trail_length)
                self.socket.send_pyobj(trail_suggestion)
            except Exception as e:
                print(e)
            else:
                print(f"Response Sent: {trail_suggestion}")

            sleep(0.1)

    def findTrail(self, trail_length=None) -> dict:
        """
        Desc:   Find the trail of length closest to the length provided.
        Args:
            trail_length (None | int | float): Length of the trail to match.
        Return:
            dict{"Name":str, "Length":float, "Elevation Gain":int}
        """
            
        if trail_length in (None, 0):
            row = randint(0, self.n_trails - 1)
        else:
            abs_lengths = numpy.abs(self.lengths - trail_length)
            row = numpy.argwhere(abs_lengths == numpy.min(abs_lengths))[0,0]

        # Return the trail data from the specified row:
        return self.hike_dataframe.row(row, named=True)
    
if __name__ == '__main__':

    SuggestionsServer()
