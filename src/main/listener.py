from abc import ABCMeta, abstractmethod

class Listener(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def listen(self, event):
        raise NotImplementedError()