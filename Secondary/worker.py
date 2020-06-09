# Simple demo of of the WS2801/SPI-like addressable RGB LED lights.
import time
import pigpio
import sys
from timeit import default_timer
from multiprocessing import shared_memory
from Utils.ledExtensions import LedExtensions


class Worker:
    def __init__(self, sector_count, sector_number, bars_per_sector):
        self.sector_count = sector_count
        self.sector_number = sector_number
        self.bars_per_sector = bars_per_sector
        self.leds = LedExtensions()

        self.led_positions = shared_memory.SharedMemory("LedData", False)
        self.led_colors = shared_memory.SharedMemory("LedColors", False)
        self.led_falloff = shared_memory.SharedMemory("LedFalloff", False)
        self.led_brightness = shared_memory.SharedMemory("LedBrightness", False)
        self.rotation_time = shared_memory.SharedMemory("RotationTime", False)

        self.__pigpio = pigpio.pi()
        self.__pigpio.callback(17, pigpio.FALLING_EDGE, self.on_magnet_pass)

    def get_rotation_time(self):
        stamp_len = self.rotation_time.buf[0]
        stamp = "0." + ''.join(str(x) for x in self.rotation_time.buf[1:int(stamp_len)])
        return float(stamp)

    def wait(self, full_rotation_time):
        if self.sector_number != 0:
            time_to_sleep = full_rotation_time / self.sector_count * self.sector_number
            time.sleep(time_to_sleep)

    def get_section_led_height(self, bar_index):
        led_height_percentage = self.led_positions.buf[(self.sector_number * self.bars_per_sector) + bar_index]
        return min(self.leds.get_led_count(), int(max(1, 1 + led_height_percentage * self.leds.get_led_count() / 100)))

    def get_section_led_color(self, bar_index):
        offset = ((self.sector_number * self.bars_per_sector) + bar_index) * 3
        return (int(self.led_colors.buf[offset]), int(self.led_colors.buf[offset + 1]), int(self.led_colors.buf[offset + 2]))

    def get_led_falloff_value(self):
        return int(self.led_falloff.buf[0])

    def get_led_brightness(self):
        brightness = str(self.led_brightness.buf[1]) + '.' + str(self.led_brightness.buf[2]) + str(self.led_brightness.buf[3])
        return float(brightness)

    def on_magnet_pass(self, gpio, level, tick):
        self.wait(self.get_rotation_time())

        bar_index = self.sector_number
        led_color = self.get_section_led_color(bar_index)
        led_falloff = self.get_led_falloff_value()
        led_brightness = self.get_led_brightness()
        section_height = self.get_section_led_height(bar_index)
        self.leds.show_range(0, section_height, led_color, led_brightness, led_falloff)


if __name__ == "__main__":
    totalThreadCount = int(sys.argv[1])
    currentThreadNumber = int(sys.argv[2])

    worker = Worker(totalThreadCount, currentThreadNumber, 1)

    try:
        while True:
            time.sleep(1)
    except:
        pass  # TODO: Find a way to quit this in a cleaner way
