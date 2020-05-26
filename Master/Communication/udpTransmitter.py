import socket


class UdpTransmitter:
    def __init__(self, destination_ip, destination_port):
        self.__destination_ip = destination_ip
        self.__destination_port = destination_port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, data):
        self.__socket.sendto(data.encode(), (self.__destination_ip, self.__destination_port))

    def send_pair(self, data_pair):
        if len(data_pair) > 2:
            raise(Exception("Data tuple is not a pair of two elements!"))
        data_list = '='.join(data_pair)
        self.__socket.sendto(data_list.encode(), (self.__destination_ip, self.__destination_port))
