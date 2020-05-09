# Simple demo of of the WS2801/SPI-like addressable RGB LED lights.
import time
import RPi.GPIO as GPIO
import sys
from timeit import default_timer

# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI

# Configure the count of pixels:
PIXEL_COUNT = 18

# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT = 0
SPI_DEVICE = 0
GPIO.setmode(GPIO.BCM)

# globals
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)
previous_timestamp = default_timer()
colors = ((255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255))
threadNumber = int(sys.argv[1])


def sensorCallback(channel):
    global previous_timestamp, pixels, colors, threadNumber
    if not (GPIO.input(channel)):
        new_stamp = default_timer()
        stamp = new_stamp - previous_timestamp
        previous_timestamp = new_stamp

        time_to_sleep = stamp / 4 * threadNumber
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)
        color = colors[threadNumber]
        for i in range(pixels.count()):
            pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(color[0], color[1], color[2]))
        pixels.show()
        pixels.clear()
        pixels.show()


if __name__ == "__main__":
    # Clear all the pixels to turn them off.
    pixels.clear()
    pixels.show()  # Make sure to call show() after changing any pixels!

    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(17, GPIO.BOTH, callback=sensorCallback)

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        GPIO.cleanup()
