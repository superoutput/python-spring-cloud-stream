from basemicroservice import BaseMicroservice
from random import randrange
from time import sleep
import os
import threading
import multiprocessing

class API(BaseMicroservice):
    def construct( self ):
        print("API.construct(): This function should be implemented.")

    def start( self ):
        self.notify(message="API.start()-%s [PID: %s, Process Name: %s, Thread Name: %s]" % (
            self._count,
            os.getpid(),
            multiprocessing.current_process().name,
            threading.current_thread().name)
        )
        #sleep(randrange(1, 5))
        sleep(1)

    def stop( self ):
        print("API.stop(): This function should be implemented.")

    def destruct( self ):
        print("API.destruct(): This function should be implemented.")