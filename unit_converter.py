"""Code Citation: ZMQ socket derived from  suggestion_service.py code by Seth Mackovjak @seth08"""
from constants import *
import zmq
from time import sleep
from datetime import datetime

class UnitConverter:
    """Converts a list of [Total Distance, Total Elevation Gain, Avg Distance, Avg Elevation] to
    from Imperial measurements to metric."""
    def __init__(self, socket=None) -> None:
        print("Server initializing... ", end="")
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind(socket or ConnectionEnum.SERVER_SOCKET1.value)
        self.listener()

    def listener(self) -> None:
        """
        Listener method continuously waiting for request. If it receives one, attempts to convert
        and sends back through socket
        """

        print("Done.")
        while True:
            # recieve object at socket and print
            units = self.socket.recv_pyobj()
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S%z'), f"Request recieved: {units}", end="\n\t")
            # try to convert and sent back
            try:
                units = self.convert(units)
                self.socket.send_pyobj(units)
            except Exception as e:
                print(e)
            else:
                print(f"Response Sent: {units}")

            sleep(0.1)

    def convert(self, units=None) -> list:
        """Takes a list of Imperial measurements and converts them to metric"""
        if units is None or len(units) != 5:
            print("Error - invalid parameter")
            return units

        units[1] = round((float(units[1]) * 1.609), 2)
        units[2] = round((float(units[2]) * .305), 2)
        units[3] = round((float(units[1]) * 1.609), 2)
        units[4] = units[2] = round((float(units[2]) * .305), 2)
        return units
        # 1 mile = 1.609km
        # 1 foot = .305 meter

if __name__ == '__main__':

    UnitConverter()
