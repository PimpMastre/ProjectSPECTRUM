import numpy as np
import pyaudio
from Utils.timerThread import TimerThread


class AudioProcessor:
    def __init__(self, nb=5, lcm=20, hcm=1024, ac=1000000, ms=0, da=200, ppbl=2, ch=2, rate=44100, chunksz=2048, vel=0.33, ar=10, udp=None):
        """
        :param nb: number of bars to interpret data with
        :param lcm: lower range chunk cut, cuts the lower ranges by fcl percent
        :param hcm: higher range chunk cut, cuts the higher ranges by fch percent
        :param ac: amplitude clip, clips the amplitude values
        :param ms: mapping style, 0 = linspace, 1 = geomspace
        :param da: data amplification, amplifies results by da percent
        :param ppbl: previous peaks buffer length, which averages current data with previous data
        :param ch: number of channels
        :param rate: sample rate
        :param chunksz: chunk size
        :param udp: UdpTransmitter object for address and port binding
        :param rip: ip address of receiver (secondary)
        :param rp: port of receiver (secondary)
        """
        self.connection = udp

        self.spectrum_data = []
        self.processed_data = []

        # data transformation parameters
        self.velocity = vel
        self.averaging_rate = ar
        self.num_bars = nb
        self.lower_chunk_margin = lcm
        self.higher_chunk_margin = hcm
        self.mapping_style = ms
        self.amplitude_clip = ac
        self.data_amplification = da
        self.prev_peaks_buffer_length = ppbl
        self.prev_peaks = [[0 for x in range(self.num_bars)] for y in range(self.prev_peaks_buffer_length)]

        # pyaudio init
        self.chunk_size = chunksz
        self.sample_rate = rate

        self.pyaudio = pyaudio.PyAudio()
        self.stream = self.pyaudio.open(
            format=pyaudio.paInt16,
            channels=ch,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
        )

    def process_stream(self):
        waveform_data = self.stream.read(self.chunk_size, False)
        waveform_data = np.frombuffer(waveform_data, dtype=np.int16)

        self.spectrum_data = abs(np.fft.fft(waveform_data).real)
        self.spectrum_data = self.spectrum_data[:int(len(self.spectrum_data) / 2)]

    def update_prev_peaks(self, new_peaks):
        self.prev_peaks.pop(0)
        self.prev_peaks.append(new_peaks)

    def get_section_average(self, section):
        highest_value_index = section.index(max(section))
        extra_values_count = self.averaging_rate * 100 // len(section)
        return np.average(section[max(0, highest_value_index - extra_values_count)],
                          min(len(section) - 1, highest_value_index + extra_values_count))

    def transform_stream(self):
        plot_points = []
        if self.mapping_style == 1:
            plot_points = np.geomspace(self.lower_chunk_margin, self.higher_chunk_margin, num=self.num_bars + 1)
        else:
            plot_points = np.linspace(self.lower_chunk_margin, self.higher_chunk_margin, num=self.num_bars + 1)

        absolute_data = np.clip(np.abs(self.spectrum_data), a_min=0, a_max=self.amplitude_clip)
        current_averages = []
        
        for x in range(self.num_bars):
            section = absolute_data[int(plot_points[x]):int(plot_points[x + 1])]

            # get average of current section
            section_average = self.get_section_average(section)
            section_average = np.average(section)
            # calculate with velocity
            distance = section_average - self.prev_peaks[len(self.prev_peaks) - 1][x]
            section_average = (self.prev_peaks[len(self.prev_peaks) - 1][x] + distance) * self.velocity
      
            # amplify
            amplification_value = self.data_amplification * section_average / 100
            current_averages.append(section_average + amplification_value)
            
        self.update_prev_peaks(np.array(current_averages))
        self.processed_data = np.average(self.prev_peaks, axis=0)

    def send_data(self):
        data = self.processed_data
        for i in range(len(data)):
            data[i] = data[i] * 100 / self.amplitude_clip
        
        data = str(list(data))
        self.connection.send(data)

    def update(self):
        self.process_stream()
        self.transform_stream()
        self.send_data()

    def start(self, interval):
        """
        Starts the processing and sending thread
        :param interval: the interval at which to process the data
        :param destination_ip: the ip of the secondary to which to send the data
        :param destination_port: the port of the secondary to which to send the data
        :return: the stop trigger for the processing thread
        """

        thread = TimerThread(self.update, interval)
        thread.start()
        return thread.get_stop_trigger()
