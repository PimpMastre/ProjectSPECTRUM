import requests
from Communication.udpTransmitter import UdpTransmitter
from audioProcessor import AudioProcessor

from Communication.udpAudioSettingsManager import UdpAudioSettingsManager

if __name__ == '__main__':
    udp_transmitter = UdpTransmitter('192.168.0.69', 6942)
    api_data = requests.get("http://192.168.0.70/master/getAll")
    audio_processor = AudioProcessor(
        nb=int(api_data.json()['numberOfBars']),
        ms=int(api_data.json()['mappingStyle']),
        hcm=int(api_data.json()['higherChunkMargin']),
        lcm=int(api_data.json()['lowerChunkMargin']),
        da=int(api_data.json()['dataAmplification']),
        ac=int(api_data.json()['amplitudeClip']),
        ppbl=int(api_data.json()['previousPeaksBufferLength']),
        vel=float(api_data.json()['velocity']),
        udp=udp_transmitter
    )
    stop_event = audio_processor.start(interval=0.001)

    setting_receiver = UdpAudioSettingsManager('192.168.0.70', 6943, audio_processor)

    try:
        setting_receiver.start_loop()
    except KeyboardInterrupt:
        print("Shutting down server...")
        stop_event.set()
