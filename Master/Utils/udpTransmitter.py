import socket


class UdpTransmitter:
    def __init__(self, bind_addr, bind_port):
        self.__bind_address = bind_addr
        self.__bind_port = bind_port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.__socket.bind((self.__bind_address, self.__bind_port))

    def send(self, data, address, port):
        self.__socket.sendto(data.encode(), (address, port))
