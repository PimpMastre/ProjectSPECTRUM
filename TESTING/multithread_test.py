# Simple demo of of the WS2801/SPI-like addressable RGB LED lights.
import time
import RPi.GPIO as GPIO
import random
import threading
from timeit import default_timer

# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI

# Configure the count of pixels:
PIXEL_COUNT = 18

# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)
GPIO.setmode(GPIO.BCM)
previous_timestamp = default_timer()


def delayedHalf(delay):
    time.sleep(delay)
    for i in range(pixels.count()):
        pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(255, 0, 0))
    pixels.show()
    pixels.clear()
    pixels.show()


def sensorCallback(channel):
    global previous_timestamp, pixels
    if not (GPIO.input(channel)):
        new_stamp = default_timer()
        stamp = new_stamp - previous_timestamp
        previous_timestamp = new_stamp
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        n = 5
        for i in range(n):
            show_stamp = default_timer()
            for i in range(pixels.count()):
                pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(r, b, g))
            pixels.show()
            pixels.clear()
            pixels.show()
            thread = threading.Thread(target=delayedHalf, args=[stamp/2])
            thread.start()
            timeTaken = default_timer() - show_stamp
            slep = (stamp - timeTaken) / (n * 2)
            # print(slep)
            time.sleep(slep)


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
