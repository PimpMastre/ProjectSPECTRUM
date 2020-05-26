import socket


class UdpAudioSettingsManager:
    def __init__(self, bind_ip, bind_port, audio_processor):
        self.__bind_ip = bind_ip
        self.__bind_port = bind_port
        self.__audio_processor = audio_processor

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.bind((self.__bind_ip, self.__bind_port))

    def update_property(self, identifier, new_value):
        if identifier == 'numberOfBars':
            self.__audio_processor.num_bars = int(new_value)
        elif identifier == 'lowerChunkMargin':
            self.__audio_processor.lower_chunk_margin = int(new_value)
        elif identifier == 'higherChunkMargin':
            self.__audio_processor.higher_chunk_margin = int(new_value)
        elif identifier == 'amplitudeClip':
            self.__audio_processor.amplitude_clip = int(new_value)
        elif identifier == 'mappingStyle':
            self.__audio_processor.mapping_style = int(new_value)
        elif identifier == 'dataAmplification':
            self.__audio_processor.data_amplification = int(new_value)
        elif identifier == 'previousPeaksBufferLength':
            self.__audio_processor.prev_peaks_buffer_length = int(new_value)
            self.__audio_processor.prev_peaks = [[0 for x in range(self.__audio_processor.num_bars)] for y in range(self.__audio_processor.prev_peaks_buffer_length)]

    def start_loop(self):
        while True:
            data, address = self.__socket.recvfrom(512)
            decoded_data = data.decode()
            identifier, value = decoded_data.split('=')
            self.update_property(identifier, value)
