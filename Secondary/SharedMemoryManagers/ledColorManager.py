from multiprocessing import shared_memory


class LedColorManager:
    def __init__(self, buffer_name="LedColors", buffer_size=256):
        self.shared_buffer = shared_memory.SharedMemory(buffer_name, True, buffer_size)

    def __del__(self):
        self.shared_buffer.close()
        self.shared_buffer.unlink()

    def update_buffer(self, color_data, index):
        self.shared_buffer.buf[index * 3] = color_data[0]
        self.shared_buffer.buf[index * 3 + 1] = color_data[1]
        self.shared_buffer.buf[index * 3 + 2] = color_data[2]
