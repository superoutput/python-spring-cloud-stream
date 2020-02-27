import os
import multiprocessing
import threading
from time import sleep
from monitor.basemicroservice import BaseMicroservice
from monitor.servicemanager import ServiceManager
from spring.streamgateway import StreamGateway
from py4j.java_gateway import JavaGateway, java_import, CallbackServerParameters


class StreamSubscriber(BaseMicroservice):
    def __init__(self, callback, *args):
        super().__init__()
        self.callback = callback
        self.args = args
        manager = ServiceManager()
        manager.register(self)


    def onMessage( self, message ):
        self.callback(message)

    def construct( self ):
        print("StreamSubscriber.construct(): This function should be implemented.")

    def start( self ):
        self.notify(message="StreamSubscriber.start()-%s [PID: %s, Process Name: %s, Thread Name: %s]" % (
            self._count,
            os.getpid(),
            multiprocessing.current_process().name,
            threading.current_thread().name)
        )
        #sleep(randrange(1, 5))
        # sleep(1)
        stream_gateway = StreamGateway(self)
        stream_gateway.start(self.args)

    def stop( self ):
        print("StreamSubscriber.stop(): This function should be implemented.")

    def destruct( self ):
        print("StreamSubscriber.destruct(): This function should be implemented.")

    def postConstruct( self ):
        # self.notify(status="Changed to PostConstruct state.", microservice="%s" % self, error=False)
        print("You can override function postConstruct().")
        pass