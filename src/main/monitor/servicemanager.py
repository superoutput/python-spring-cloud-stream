import sys
from monitor.listener import Listener
from monitor.microservice import Microservice
from monitor.workerpool import WorkerPool

class ServiceManager(Listener):

    def __init__(self):
        # print("Self: %s" % str(self))
        self._microservices = []
        self.pool = WorkerPool()

    def register(self, microservice):
        if not isinstance(microservice, Microservice): raise Exception('Unsupported interface')
        if not Microservice.version() == '2.0': raise Exception('Unsupported version')

        self._microservices.append(microservice)
        microservice.subscribe(self)
        self.pool.add(microservice)

    def unregister(self, microservice):
        self.pool.stop(microservice)
        if microservice in self._microservices:
            self._microservices.remove(microservice)

    def pause(self, index):
        self.pool.pause(index)

    def resume(self, index):
        self.pool.resume(index)

    def stop(self, index):
        self.pool.stop(index)

    def exit(self):
        self.pool.exit()

    def list(self):
        return self._microservices

    def test(self):
        for _microservice in self._microservices:
            _microservice.init()
            _microservice.destroy()
            #print(_microservice.version())

    def listen(self, event):
        #print('[%s] Event : %s ' % (event.microservice, event.status))
        pass

