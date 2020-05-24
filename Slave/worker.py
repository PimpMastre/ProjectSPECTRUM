# Simple demo of of the WS2801/SPI-like addressable RGB LED lights.
import time
import RPi.GPIO as GPIO
import sys
from multiprocessing import shared_memory
from Slave.Utils.ledExtensions import LedExtensions


class Worker:
    def __init__(self, sector_count, sector_number, bars_per_sector):
        self.sector_count = sector_count
        self.sector_number = sector_number
        self.bars_per_sector = bars_per_sector
        self.leds = LedExtensions()

        self.led_positions = shared_memory.SharedMemory("LedPositions", False)
        self.led_colors = shared_memory.SharedMemory("LedColors", False)
        self.rotation_time = shared_memory.SharedMemory("RotationTime", False)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(17, GPIO.RISING, callback=self.on_magnet_pass, bouncetime=0)

    def get_rotation_time(self):
        stamp_len = self.rotation_time.buf[0]
        stamp = "0." + ''.join(str(x) for x in self.rotation_time.buf[1:int(stamp_len)])
        return float(stamp)

    def wait(self, full_rotation_time):
        time_to_sleep = full_rotation_time / self.sector_number * self.sector_number
        if self.sector_number != 0:
            time.sleep(time_to_sleep)

    def get_section_led_height(self, bar_index):
        led_height_percentage = self.led_positions.buf[(self.sector_number * self.bars_per_sector) + bar_index]
        return min(self.leds.get_led_count(), int(led_height_percentage * self.leds.get_led_count() / 100))

    def get_section_led_color(self, bar_index):
        offset = ((self.sector_number * self.bars_per_sector) + bar_index) * 3
        return self.led_positions.buf[offset:offset+2]

    def on_magnet_pass(self):
        self.wait(self.get_rotation_time())

        for bar_index in range(self.bars_per_sector):
            led_color = self.get_section_led_color(bar_index)
            section_height = self.get_section_led_height(self.sector_number)

            self.leds.show_range(0, section_height, led_color, 0)


if __name__ == "__main__":
    totalThreadCount = int(sys.argv[1])
    currentThreadNumber = int(sys.argv[2])

    worker = Worker(totalThreadCount, currentThreadNumber, 1)

    try:
        while True:
            time.sleep(0.1)
    except:
        pass  # TODO: Find a way to quit this in a cleaner way
