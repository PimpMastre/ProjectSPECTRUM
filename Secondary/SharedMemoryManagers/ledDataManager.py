from multiprocessing import shared_memory


class LedDataManager:
    def __init__(self, buffer_name="LedData", buffer_size=256):
        self.shared_buffer = shared_memory.SharedMemory(buffer_name, True, buffer_size)

    def __del__(self):
        self.shared_buffer.close()
        self.shared_buffer.unlink()

    def update_buffer(self, data):
        for i in range(len(data)):
            self.shared_buffer.buf[i] = int(data[i])
