from multiprocessing import shared_memory
import struct

class RotationTimeManager:
    def __init__(self, buffer_name="RotationTime", buffer_size=64):
        self.shared_buffer = shared_memory.SharedMemory(buffer_name, True, buffer_size)

    def __del__(self):
        self.shared_buffer.close()
        self.shared_buffer.unlink()

    def update_buffer(self, duration_timestamp):
        """
        Updates the shared buffer with a new duration. it sends only the fractional part
        :param duration_timestamp: a float representing the duration of a rotation
        """
        timestamp_bytes = bytearray(struct.pack("f", duration_timestamp))
        self.shared_buffer.buf[:len(duration_timestamp)] = timestamp_bytes
