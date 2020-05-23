# Simple demo of of the WS2801/SPI-like addressable RGB LED lights.
import time
import RPi.GPIO as GPIO
import sys
import random
from timeit import default_timer
from multiprocessing import shared_memory

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
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255),
          (0, 0, 255), (0, 255, 0), (0, 0, 255), (255, 255, 255),
          (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255),
          (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)]
#color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
totalThreadCount = int(sys.argv[1])
currentThreadNumber = int(sys.argv[2])
shared = shared_memory.SharedMemory("LedPositions", False)
rotationTime = shared_memory.SharedMemory("RotationTime", False)
bars_per_sector = 1


def sensorCallback(channel):
    global previous_timestamp, pixels, currentThreadNumber, totalThreadCount, shared, bars_per_sector
    if not (GPIO.input(channel)) or GPIO.input(channel):
        #pixels.clear()
        #new_stamp = default_timer()
        #stamp = new_stamp - previous_timestamp
        #previous_timestamp = new_stamp
        stamp_len = rotationTime.buf[0]
        stamp = "0."
        for i in range(stamp_len):
            stamp += str(rotationTime.buf[i + 1])
        stamp = float(stamp)

        time_to_sleep = stamp / totalThreadCount * currentThreadNumber
        if currentThreadNumber > 0:
            #print(time_to_sleep)
            time.sleep(time_to_sleep)
        led_height_percentage = shared.buf[currentThreadNumber]
        current_led = min(18, int(led_height_percentage * 18 / 100))
        #print(current_led)
        for k in range(bars_per_sector):
            color = colors[0] # colors[(currentThreadNumber * bars_per_sector) + k]
            #led_height_percentage = shared.buf[(currentThreadNumber * 2) + k]
            #current_led = min(18, int(led_height_percentage * 18 / 100))
            pixels.clear()
            for i in range(current_led):
                pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(color[0], color[1], color[2]))
            pixels.show()
            #pixels.clear()
            #pixels.show()
        #pixels.clear()
        #pixels.show()


if __name__ == "__main__":
    # Clear all the pixels to turn them off.
    pixels.clear()
    pixels.show()  # Make sure to call show() after changing any pixels!

    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(17, GPIO.RISING, callback=sensorCallback, bouncetime=10)

    try:
        while True:
            time.sleep(0.1)
    except:
        GPIO.cleanup()
        shared.close()
        rotationTime.close()
