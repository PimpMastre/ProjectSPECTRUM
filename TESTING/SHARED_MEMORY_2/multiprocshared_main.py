import sys
import time
import subprocess
import random
from multiprocessing import shared_memory

if __name__ == "__main__":
    # cmdline arguments
    total_threads = int(sys.argv[1])
    led_speed = int(sys.argv[2])

    processIds = []
    for i in range(int(total_threads)):
        command = 'python multiprocshared_worker.py ' + str(total_threads) + ' ' + str(i) + ' &'
        print('running command \"' + command + '\"...')
        pid = subprocess.Popen(command.split(' '))
        processIds.append(pid)

    rising = True
    currentLed = random.randint(0, 16)

    # shared buffer
    shared = shared_memory.SharedMemory("LedPositions", True, 512)

    try:
        while True:
            if rising:
                currentLed += led_speed
                if currentLed > 17:
                    currentLed = 18 - (currentLed - 18)
                    rising = False
            else:
                currentLed -= led_speed
                if currentLed < 0:
                    currentLed = -currentLed
                    rising = True

            shared.buf[0] = currentLed
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Killing spawned processes...")
        #for pid in processIds:
         #   subprocess.call(["kill", str(pid)])
         #   print("Process " + str(pid) + " successfully killed.")
