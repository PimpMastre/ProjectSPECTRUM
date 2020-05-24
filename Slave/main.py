import sys

from Slave.master import Master

if __name__ == "__main__":
    # command line argument
    total_threads = int(sys.argv[1])
    master = Master("192.168.0.69", 6942, thread_count=total_threads)

    try:
        master.start_loop()
    except KeyboardInterrupt:
        print("Stopping everything...")
