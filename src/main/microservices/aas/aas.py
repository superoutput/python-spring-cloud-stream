from basemicroservice import BaseMicroservice
from random import randrange
from time import sleep
import os
import threading
import multiprocessing

class AAS(BaseMicroservice):
    def construct( self ):
        print("AAS.construct(): This function should be implemented.")

    def start( self ):
        self.notify(message="AAS.start()-%s [PID: %s, Process Name: %s, Thread Name: %s]" % (
            self._count,
            os.getpid(),
            multiprocessing.current_process().name,
            threading.current_thread().name)
        )
        #sleep(randrange(1, 5))
        sleep(1)

    def stop( self ):
        print("AAS.stop(): This function should be implemented.")

    def destruct( self ):
        print("AAS.destruct(): This function should be implemented.")