from abc import ABCMeta, abstractmethod

class Microservice:
    __metaclass__ = ABCMeta

    @classmethod
    def version(self): return "2.0"

    @abstractmethod
    def construct(self): pass
    
    @abstractmethod
    def start(self): raise NotImplementedError
    
    @abstractmethod
    def stop(self): raise NotImplementedError
    
    @abstractmethod
    def destruct(self): raise NotImplementedError