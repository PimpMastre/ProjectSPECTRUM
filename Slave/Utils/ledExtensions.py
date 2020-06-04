import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO

class LedExtensions:
    def __init__(self, led_count=18, spi_port=0, spi_device=0):
        self.leds = Adafruit_WS2801.WS2801Pixels(led_count, spi=SPI.SpiDev(spi_port, spi_device), gpio=GPIO)
        self.led_count = led_count

        '''
            not sure if all WS2801 strips are like this or if the Adafruit package is broken, but green and blue
            colors are switched in my case.
        '''
        self.__red_index = 0
        self.__green_index = 2
        self.__blue_index = 1

    def show_range(self, start, end, color, brightness=1, falloff=0):
        for i in range(start, end - falloff):
            self.leds.set_pixel(i, Adafruit_WS2801.RGB_to_color(int(color[self.__red_index] * brightness),
                                                                int(color[self.__green_index] * brightness),
                                                                int(color[self.__blue_index] * brightness)))

        for i in range(max(start, end - falloff), end):
            color_falloff = min(1.0 / (falloff + 1) * (end - i), 1)
            self.leds.set_pixel(i, Adafruit_WS2801.RGB_to_color(int((color[self.__red_index] * brightness) * color_falloff),
                                                                int((color[self.__green_index] * brightness) * color_falloff),
                                                                int((color[self.__blue_index] * brightness) * color_falloff)))

        for i in range(end, self.led_count):
            self.leds.set_pixel(i, Adafruit_WS2801.RGB_to_color(0, 0, 0))

        self.leds.show()

    def clear(self):
        self.leds.clear()
        self.leds.show()

    def get_led_count(self):
        return self.led_count
