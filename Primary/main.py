import requests
from Communication.udpTransmitter import UdpTransmitter
from audioProcessor import AudioProcessor

from Communication.udpPrimarySettingsManager import UdpPrimarySettingsManager

from motorController import MotorController

if __name__ == '__main__':
    udp_transmitter = UdpTransmitter('192.168.0.69', 6942)
    api_data = requests.get("http://192.168.0.70:5000/master/getAll")
    audio_processor = AudioProcessor(
        nb=int(api_data.json()['numberOfBars']),
        ms=int(api_data.json()['mappingStyle']),
        hcm=int(api_data.json()['higherChunkMargin']),
        lcm=int(api_data.json()['lowerChunkMargin']),
        da=int(api_data.json()['dataAmplification']),
        ac=int(api_data.json()['amplitudeClip']),
        ppbl=int(api_data.json()['previousPeaksBufferLength']),
        vel=float(api_data.json()['velocity']) / 100,
        udp=udp_transmitter
    )
    stop_event = audio_processor.start(interval=0.001)

    motorController = MotorController()
    setting_receiver = UdpPrimarySettingsManager('192.168.0.70', 6943, audio_processor, motorController)

    try:
        setting_receiver.start_loop()
    except KeyboardInterrupt:
        print("Shutting down server...")
        stop_event.set()
