import sys
import time
import subprocess
import random
from multiprocessing import shared_memory
import numpy as np
import pyaudio
from pyqtgraph.Qt import QtCore


class BarVisualiser:
    def __init__(self, shared_mem):
        self.shared_buffer = shared_mem

        self.wf_data = []
        self.fft_data = []
        self.frequency_data = []

        self.num_bars = 6
        self.max_bar_height = 18
        self.frequency_cut = 50

        self.prev_peaks_buffer_length = 2
        self.prev_peaks = [[0 for x in range(self.num_bars)] for y in range(self.prev_peaks_buffer_length)]

        # pyaudio stuff
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.CHUNK = 1024 * 2

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
        )

    def process_stream(self):
        self.wf_data = self.stream.read(self.CHUNK, False)
        self.wf_data = np.frombuffer(self.wf_data, dtype=np.int16)

        self.fft_data = abs(np.fft.fft(self.wf_data).real)
        self.fft_data = self.fft_data[:int(len(self.fft_data) / 2)]
        self.frequency_data = np.fft.fftfreq(self.CHUNK, 1.0 / self.RATE)
        self.frequency_data = self.frequency_data[:int(len(self.frequency_data) / 2)]


    def update_prev_peaks(self, new_peaks):
        self.prev_peaks.pop(0)
        self.prev_peaks.append(new_peaks)

    def update_fft(self):
        self.process_stream()
        # MAYBE ADD FREQUENCY CUTTING/EQUALIZER
        cut = int((self.CHUNK / 2) * self.frequency_cut / 100)
        test = np.geomspace(20, cut, num=self.num_bars)
        # test = np.linspace(20, cut, num=self.num_bars)
        # spec_width = self.CHUNK // self.num_bars
        # clip to 1M, get percentages for display
        self.fft_data = np.clip(self.fft_data, a_min=0, a_max=1000000)

        absolute_fft_data = np.abs(self.fft_data)
        section = absolute_fft_data[:int(test[0])]
        averages = [np.average(section) * 100 / 1000000]
        for x in range(self.num_bars - 1):
            section = absolute_fft_data[int(test[x]):int(test[x + 1])]
            avg = np.average(section) * 100 / 1000000
            averages.append(avg)

        self.update_prev_peaks(np.array(averages))
        averages = np.average(self.prev_peaks, axis=0)

        for j in range(len(averages)):
            self.shared_buffer[j] = averages[j]

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update_fft)
        timer.start(10)


if __name__ == "__main__":
    # cmdline arguments
    total_threads = int(sys.argv[1])
    led_speed = int(sys.argv[2])

    processIds = []
    for i in range(int(total_threads)):
        command = 'python multiprocshared_worker.py ' + str(total_threads) + ' ' + str(i) + ' &'
        print('running command \"' + command + '\"...')
        pid = subprocess.Popen(command.split(' '))
        processIds.append(pid)

    rising = True
    currentLed = random.randint(0, 16)

    # shared buffer
    shared = shared_memory.SharedMemory("LedPositions", True, 512)

    visualiser = BarVisualiser(shared)
    visualiser.animation()

    except KeyboardInterrupt:
        print("Killing spawned processes...")