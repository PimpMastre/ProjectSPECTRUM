import sys
import subprocess
import random
import time
import socket
from multiprocessing import shared_memory
import RPi.GPIO as GPIO
from timeit import default_timer

timing = shared_memory.SharedMemory("RotationTime", True, 64)
prev_timestamp = default_timer()


def sensorCallback(channel):
    global prev_timestamp
    new_stamp = default_timer()
    stamp = new_stamp - prev_timestamp
    prev_timestamp = new_stamp
    #print(stamp)
    stamp = str(stamp)[2:]
    timing.buf[0] = len(stamp)
    for i in range(len(stamp)):
        timing.buf[i + 1] = int(stamp[i])

if __name__ == "__main__":
    # cmdline arguments
    total_threads = int(sys.argv[1])
    #led_speed = int(sys.argv[2])

    processIds = []
    for i in range(int(total_threads)):
        command = 'python multiprocshared_worker.py ' + str(total_threads) + ' ' + str(i) + ' &'
        print('running command \"' + command + '\"...')
        pid = subprocess.Popen(command.split(' '))
        processIds.append(pid)

    print('Successfully started processes with pids: ')
    for pidobj in processIds:
        print(pidobj.pid)

    rising = True
    currentLed = random.randint(0, 16)

    shared = shared_memory.SharedMemory("LedPositions", True, 128)

    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1)
    sock.setblocking(0)
    sock.bind(("192.168.0.69", 6942))

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(17, GPIO.BOTH, callback=sensorCallback)

    try:
        while True:
            time.sleep(0.01)
            try:
                data, addr = sock.recvfrom(512)
                sock.settimeout(0)
                decoded_data = eval(data.decode('utf-8'))
                #print(decoded_data)
                for i in range(len(decoded_data)):
                    shared.buf[i] = int(decoded_data[i])
                sock.settimeout(60)
            except socket.error as e:
                pass
    except KeyboardInterrupt:
        print("Clearing shared memory...")
        shared.close()
        shared.unlink()
        timing.close()
        timing.unlink()
        print("Killing spawned processes...")
