#!/usr/bin/env python3

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import sys
import pyaudio


class BarVisualiser:
    def __init__(self):
        self.window = pg.plot()
        self.window.setWindowTitle('Bar Visualiser')

        self.wf_data = []
        self.fft_data = []
        self.frequency_data = []

        self.num_bars = 35
        self.x_axis = np.arange(self.num_bars)
        self.y_axis = None

        self.prev_peaks_buffer_length = 3
        self.prev_peaks = [[0 for x in range(self.num_bars)] for y in range(self.prev_peaks_buffer_length)]
        self.collection_percentage = 10

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

        self.bar_graph = pg.BarGraphItem(x=self.x_axis, height=[0 for x in range(self.num_bars)], width=0.6, brush='r')
        self.window.addItem(self.bar_graph)

    def start(self):
        if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def process_stream(self):
        self.wf_data = self.stream.read(self.CHUNK, False)
        self.wf_data = np.frombuffer(self.wf_data, dtype=np.int16)

        self.fft_data = abs(np.fft.fft(self.wf_data).real)
        self.fft_data = self.fft_data[:int(len(self.fft_data) / 2)]
        self.frequency_data = np.fft.fftfreq(self.CHUNK, 1.0 / self.RATE)
        self.frequency_data = self.frequency_data[:int(len(self.frequency_data) / 2)]

    def update(self):
        peaks = []
        spec_width = self.CHUNK // self.num_bars
        wf_data = self.stream.read(self.CHUNK)
        wf_data = np.frombuffer(wf_data, dtype=np.int16)
        for x in range(self.num_bars):
            peaks.append(np.average(np.abs(wf_data)[x * spec_width:(x + 1) * spec_width]))

        self.bar_graph.setOpts(x=self.x_axis, height=np.array(peaks))

    def update_prev_peaks(self, new_peaks):
        self.prev_peaks.pop(0)
        self.prev_peaks.append(new_peaks)

    def update_fft(self):
        self.process_stream()
        test = np.geomspace(20, self.CHUNK / 2, num=self.num_bars)
        # spec_width = self.CHUNK // self.num_bars
        absolute_fft_data = np.abs(self.fft_data)
        n = len(absolute_fft_data) * self.collection_percentage / 100
        averaged_percent = np.average(absolute_fft_data[int(test[x]):int(test[x + 1])].argsort()[::-1][:n])
        averages = [averaged_percent]
        # self.fft_data = np.clip(self.fft_data, a_min=0, a_max=500000)
        for x in range(self.num_bars - 1):
            n = len(absolute_fft_data) * self.collection_percentage / 100
            averaged_percent = np.average(absolute_fft_data[int(test[x]):int(test[x + 1])].argsort()[::-1][:n])
            averages.append(averaged_percent)

        self.update_prev_peaks(np.array(averages))
        averages = np.average(self.prev_peaks, axis=0)

        self.bar_graph.setOpts(height=np.array(averages))

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update_fft)
        timer.start(10)
        self.start()


if __name__ == '__main__':
    visualiser = BarVisualiser()
    visualiser.animation()
