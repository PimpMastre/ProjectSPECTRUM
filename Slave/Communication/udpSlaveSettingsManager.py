import socket


class UdpSlaveSettingsManager:
    def __init__(self, bind_ip, bind_port, color_data_manager, falloff_data_manager):
        self.__bind_ip = bind_ip
        self.__bind_port = bind_port
        self.__color_data_manager = color_data_manager
        self.__falloff_data_manager = falloff_data_manager

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.bind((self.__bind_ip, self.__bind_port))

    def update_property(self, identifier, new_value):
        if identifier == 'colors':
            color_values = new_value.split(',')
            for i in range(0, len(color_values), 3):
                color = (int(color_values[i]), int(color_values[i + 1]), int(color_values[i + 2]))
                self.__color_data_manager.update_buffer(color, i // 3)
        elif identifier == 'ledFalloff':
            self.__falloff_data_manager.update_buffer(int(new_value))

    def start_loop(self):
        while True:
            data, address = self.__socket.recvfrom(512)
            decoded_data = data.decode()
            identifier, value = decoded_data.split('=')
            self.update_property(identifier, value)
