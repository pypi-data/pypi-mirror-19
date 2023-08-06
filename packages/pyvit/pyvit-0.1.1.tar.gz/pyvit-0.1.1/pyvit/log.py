from . import can
from multiprocessing import Queue


class Logger:
    def __init__(self, dispatcher):
        self._dispatcher = dispatcher
        self._buffer = []
        self._rx_queue = Queue()
        dispatcher.add_receiver(self._rx_queue)

    def collect(self):
        result = []
        for i in range(0, self._rx_queue.qsize()):
            result.append(self._rx_queue.get())
        return result
