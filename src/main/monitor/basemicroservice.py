from monitor.microservice import Microservice
from monitor.eventhandler import EventHandler
from monitorables.monitorable import Monitorable
# from worker import Worker

class BaseMicroservice( Microservice, EventHandler ):
    _count = 0
    _monitorables = []
    #_monitorables = [Monitorable()]

    def run(self, thread):
        self._count = 1
        while True:
            self.start()
            thread.wait(1)
            self._count+=1

    def add_listener(self, monitorable):
        # worker = Worker(monitorable.fire)
        # worker.start()
        self.subscribe(monitorable)
        self._monitorables.append(monitorable)

    def remove_listener(self, monitorable):
        self._monitorables.remove(monitorable)

    def construct( self ):
        self.notify(status="inited", microservice="%s" % self, error=False)
        pass

    def start( self ):
        #self.notify(status="started", microservice="%s" % self, error=False)
        pass

    def stop( self ):
        self.notify(status="stopped", microservice="%s" % self, error=False)
        pass

    def destruct( self ):
        self.notify(status="destroyed", microservice="%s" % self, error=False)
        pass

    def postConstruct( self ):
        # self.notify(status="Changed to PostConstruct state.", microservice="%s" % self, error=False)
        print("Changed to PostConstruct state. You can override function postConstruct().")
        pass

    def preDestroy( self ):
        # self.notify(status="Changed to PreDestroy state.", microservice="%s" % self, error=False)
        print("Changed to PreDestroy state. You can override function preDestroy().")
        pass