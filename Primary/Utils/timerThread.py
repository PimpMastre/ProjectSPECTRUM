from threading import Thread, Event


class TimerThread(Thread):
    '''
        TimerThread is a timer class that spawns a thread at a given interval
    '''
    def __init__(self, func, interval):
        """
        :param func: the function to be called every 'interval' seconds
        :param interval: the interval at which the function should be called
        """
        Thread.__init__(self)
        self.stop_trigger = Event()
        self.function_call = func
        self.interval = interval

    def run(self):
        while not self.stop_trigger.wait(self.interval):
            self.function_call()

    def get_stop_trigger(self):
        return self.stop_trigger
