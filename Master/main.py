import time
from Utils.udpTransmitter import UdpTransmitter
from audioProcessor import AudioProcessor

from Master.Communication.udpAudioSettingsManager import UdpAudioSettingsManager

if __name__ == '__main__':
    udp_transmitter = UdpTransmitter('192.168.0.69', 6942)
    audio_processor = AudioProcessor(
        nb=5,
        ms=0,
        udp=udp_transmitter
    )
    stop_event = audio_processor.start(interval=0.001)

    setting_receiver = UdpAudioSettingsManager('192.168.0.70', 6943, audio_processor)

    try:
        setting_receiver.start_loop()
    except KeyboardInterrupt:
        print("Shutting down server...")
        stop_event.set()
