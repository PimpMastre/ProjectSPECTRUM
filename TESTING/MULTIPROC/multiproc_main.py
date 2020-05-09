import os
import sys
import time
import subprocess

if __name__ == "__main__":
    total_threads = sys.argv[1]
    processIds = []
    for i in range(int(total_threads)):
        command = 'python multiproc_worker ' + total_threads + ' ' + str(i) + ' &'
        print('running command \"' + command + '\"...')
        pid = os.spawnl(os.P_NOWAIT, command)
        processIds.append(pid)

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Killing spawned processes...")
        for pid in processIds:
            subprocess.call(["kill", str(pid)])
            print("Process " + str(pid) + " successfully killed.")
