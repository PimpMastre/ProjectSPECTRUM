import time
import datetime
import RPi.GPIO as GPIO
from timeit import default_timer

previous_timestamp = default_timer()
out = open("speeds.txt", "w")

def sensorCallback(channel):
  if not(GPIO.input(channel)):
    global previous_timestamp,out
    # Called if sensor output changes
    new_stamp = default_timer()
    stamp = new_stamp - previous_timestamp
    previous_timestamp = new_stamp
    if not GPIO.input(channel):
      # Magnet
      #out.write(str(round(60/stamp)) + 'RPM\n')
      print(str(round(60/stamp)) + 'RPM: ' + str(stamp))

def main():
  # Wrap main content in a try block so we can
  # catch the user pressing CTRL-C and run the
  # GPIO cleanup function. This will also prevent
  # the user seeing lots of unnecessary error
  # messages.

  # Get initial reading
  sensorCallback(17)

  try:
    # Loop until users quits with CTRL-C
    while True :
      time.sleep(0.1)

  except KeyboardInterrupt:
    # Reset GPIO settings
    GPIO.cleanup()

# Tell GPIO library to use GPIO references
GPIO.setmode(GPIO.BCM)

print("Setup GPIO pin as input on GPIO17")

# Set Switch GPIO as input
# Pull high by default
GPIO.setup(17 , GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(17, GPIO.BOTH, callback=sensorCallback)

if __name__=="__main__":
   main()
