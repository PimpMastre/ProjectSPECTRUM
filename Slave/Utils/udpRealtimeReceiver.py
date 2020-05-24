import socket


class UdpRealtimeReceiver:
    def __init__(self, bind_addr, bind_port):
        self.__bind_address = bind_addr
        self.__bind_port = bind_port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1)
        self.__socket.setblocking(False)
        self.__socket.bind((self.__bind_address, self.__bind_port))

    def receive_current(self, buffer_size):
        self.__socket.settimeout(60)
        data, address = self.__socket.recvfrom(buffer_size)
        self.__socket.settimeout(0)

        return data
