from enum import Enum

class ConnectionEnum(Enum):
    """
    Desc: Default, uneditable values to be used unless 
            manually defined when creating the objects.
    """
    CLIENT_SOCKET="tcp://localhost:1234"
    SERVER_SOCKET="tcp://*:1234"
    CLIENT_SOCKET1 = "tcp://localhost:1235"
    SERVER_SOCKET1="tcp://*:1235"
    CLIENT_SOCKET2 = "tcp://localhost:1236"
    SERVER_SOCKET2="tcp://*:1236"
    CLIENT_SOCKET3 = "tcp://localhost:1237"
    SERVER_SOCKET3="tcp://*:1237"