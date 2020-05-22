import sys
import subprocess
import random


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

    #except KeyboardInterrupt:
     #   print("Killing spawned processes...")
