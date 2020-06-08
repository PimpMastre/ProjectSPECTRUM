import requests
import subprocess
import pigpio
from timeit import default_timer

from SharedMemoryManagers.ledColorManager import LedColorManager
from SharedMemoryManagers.ledDataManager import LedDataManager
from SharedMemoryManagers.rotationTimeManager import RotationTimeManager
from SharedMemoryManagers.ledFalloffManager import LedFalloffManager
from SharedMemoryManagers.ledFalloffManager import LedBrightnessManager

from Communication.udpRealtimeReceiverThread import UdpRealtimeReceiverThread
from Communication.udpSlaveSettingsManager import UdpSlaveSettingsManager


class Master:
    def __init__(self, thread_count=5):
        self.thread_count = thread_count
        self.previous_timestamp = default_timer()

        # shared data managers
        self.rotation_time_manager = RotationTimeManager()
        self.led_data_manager = LedDataManager()
        self.led_color_manager = LedColorManager()
        self.led_falloff_manager = LedFalloffManager()
        self.led_brightness_manager = LedBrightnessManager()

        self.__pigpio = pigpio.pi()

    def on_magnet_pass(self, x):
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
        self.__pigpio.callback(17, pigpio.FALLING_EDGE, self.on_magnet_pass)
        #GPIO.setmode(GPIO.BCM)
        #GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #GPIO.add_event_detect(17, GPIO.FALLING, callback=self.on_magnet_pass, bouncetime=1)

    def start_loop(self):
        self.start_workers()
        self.start_magnet_detection()

        api_data = requests.get("http://192.168.0.70/master/getAll")
        api_colors = api_data.json()['colors'].split(',')
        for i in range(len(api_colors) // 3):
            red = api_colors[i * 3]
            green = api_colors[i * 3 + 1]
            blue = api_colors[i * 3 + 2]
            self.led_color_manager.update_buffer((red, green, blue), i)

        self.led_falloff_manager.update_buffer(int(api_data.json()['ledFalloff']))
        self.led_brightness_manager.update_brightness(float(api_data.json()['brightness']))

        led_data_thread = UdpRealtimeReceiverThread("192.168.0.69", 6942, self.led_data_manager)
        led_data_thread.start()
        settings_manager = UdpSlaveSettingsManager("192.168.0.69", 6943, self.led_color_manager, self.led_falloff_manager, self.led_brightness_manager)

        try:
            settings_manager.start_loop()
        except KeyboardInterrupt:
            print("Shutting Down...")
