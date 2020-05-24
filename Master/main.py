#!/usr/bin/env python3
import time
from Master.Utils.udpTransmitter import UdpTransmitter
from Master.audioProcessor import AudioProcessor

if __name__ == '__main__':
    udp_transmitter = UdpTransmitter("192.168.0.70", 6942)
    audio_processor = AudioProcessor(
        nb=5,
        ms=0,
        udp=udp_transmitter
    )
    stop_event = audio_processor.start(interval=0.001, destination_ip="192.168.0.69", destination_port=6942)

    try:
        while True:
            time.sleep(0.001)  # TODO: figure out if this is needed
    except KeyboardInterrupt:
        print("Shutting down server...")
        stop_event.set()
