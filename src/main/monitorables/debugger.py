from monitorables.monitorable import Monitorable
from queue import Queue
import sys

class Debugger(Monitorable):
    def __init__(self, microservice, out):
        super().__init__(microservice)
        self._out = out
        self._messages = Queue()

    def fire(self, thread):
        while True:
            #print('Size: %s'%self._messages.qsize())
            _f = open(self._out, 'a+')
            if not self._messages.empty():
                message = self._messages.get()
                _f.write('%s\n' % message)
            thread.wait(1)
            _f.close()

    def listen(self, event):
        self._messages.put(event.message)