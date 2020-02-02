from basemicroservice import BaseMicroservice
from random import randrange
from time import sleep
import os
import threading
import multiprocessing

class Valet(BaseMicroservice):
    def construct( self ):
        super().construct()
        print("Valet.construct(): This function should be implemented.")

    def start( self ):
        super().start()
        print("Valet.start()-%s [PID: %s, Process Name: %s, Thread Name: %s]" % (
            self._count,
            os.getpid(),
            multiprocessing.current_process().name,
            threading.current_thread().name)
        )
        #sleep(randrange(1, 5))
        sleep(1)

    def stop( self ):
        super().stop()
        print("Valet.stop(): This function should be implemented.")

    def destruct( self ):
        super().destruct()
        print("Valet.destruct(): This function should be implemented.")