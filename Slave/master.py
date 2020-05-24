import socket
import time
import subprocess
import RPi.GPIO as GPIO
from timeit import default_timer

from Slave.SharedMemoryManagers.ledColorManager import LedColorManager
from Slave.SharedMemoryManagers.ledDataManager import LedDataManager
from Slave.SharedMemoryManagers.rotationTimeManager import RotationTimeManager
from Slave.Utils.udpRealtimeReceiver import UdpRealtimeReceiver


class Master:
    def __init__(self, bind_address, bind_port, thread_count=5):
        self.thread_count = thread_count
        self.previous_timestamp = default_timer()

        self.udp_receiver = UdpRealtimeReceiver(bind_address, bind_port)

        # shared data managers
        self.rotation_time_manager = RotationTimeManager()
        self.led_data_manager = LedDataManager()
        self.led_color_manager = LedColorManager()

    def on_magnet_pass(self):
        new_stamp = default_timer()
        stamp = new_stamp - self.previous_timestamp
        self.previous_timestamp = new_stamp

        self.rotation_time_manager.update_buffer(stamp)

    def start_workers(self):
        process_ids = []
        for i in range(self.thread_count):
            command = 'python worker.py ' + str(self.thread_count) + ' ' + str(i) + ' &'
            print('running command \"' + command + '\"...')
            pid = subprocess.Popen(command.split(' '))
            process_ids.append(pid)

        print('Successfully started worker processes with pids: ')
        for pidobj in process_ids:
            print(pidobj.pid)

    def start_magnet_detection(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(17, GPIO.BOTH, callback=self.on_magnet_pass)

    def start_loop(self):
        self.start_workers()
        self.start_magnet_detection()

        self.led_color_manager.update_buffer((255, 0, 0), 0)
        self.led_color_manager.update_buffer((0, 255, 0), 1)
        self.led_color_manager.update_buffer((0, 0, 255), 2)
        self.led_color_manager.update_buffer((255, 255, 255), 3)
        self.led_color_manager.update_buffer((0, 0, 255), 4)

        while True:
            time.sleep(0.01)
            try:
                decoded_data = eval(self.udp_receiver.receive_current(512).decode('utf-8'))
                self.led_data_manager.update_buffer(decoded_data)
            except socket.error as e:
                pass
