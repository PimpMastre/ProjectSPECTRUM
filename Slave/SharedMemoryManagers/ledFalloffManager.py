from multiprocessing import shared_memory


class LedFalloffManager:
    def __init__(self, buffer_name="LedFalloff", buffer_size=32):
        self.shared_buffer = shared_memory.SharedMemory(buffer_name, True, buffer_size)

    def __del__(self):
        self.shared_buffer.close()
        self.shared_buffer.unlink()

    def update_buffer(self, data):
        self.shared_buffer.buf[0] = data
