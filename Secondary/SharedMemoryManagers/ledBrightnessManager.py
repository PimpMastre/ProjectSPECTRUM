from multiprocessing import shared_memory
import struct


class LedBrightnessManager:
    def __init__(self, buffer_name="LedBrightness", buffer_size=32):
        self.shared_buffer = shared_memory.SharedMemory(buffer_name, True, buffer_size)

    def __del__(self):
        self.shared_buffer.close()
        self.shared_buffer.unlink()

    def update_buffer(self, brightness):
        brightness_bytes = bytearray(struct.pack("f", brightness))

        self.shared_buffer.buf[:len(brightness_bytes)] = brightness_bytes
