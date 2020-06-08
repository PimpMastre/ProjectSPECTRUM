from multiprocessing import shared_memory


class LedBrightnessManager:
    def __init__(self, buffer_name="LedBrightness", buffer_size=32):
        self.shared_buffer = shared_memory.SharedMemory(buffer_name, True, buffer_size)

    def __del__(self):
        self.shared_buffer.close()
        self.shared_buffer.unlink()

    def update_buffer(self, brightness):
        length = len(str(brightness))
        self.shared_buffer.buf[0] = 3
        if int(brightness) != brightness:
            self.shared_buffer.buf[1] = int(str(brightness)[0])
            self.shared_buffer.buf[2] = int(str(brightness)[2])
            self.shared_buffer.buf[3] = int(str(brightness)[3])
        else:
            self.shared_buffer.buf[1] = int(str(brightness)[0])
            self.shared_buffer.buf[2] = 0
            self.shared_buffer.buf[3] = 0
