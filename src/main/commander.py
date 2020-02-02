import sys
from listener import Listener
from microservice import Microservice
from microservicefactory import MicroserviceFactory
from microserviceenum import MicroserviceEnum
from workerpool import WorkerPool
from microservices.aas.aas import AAS
from monitorables.tracer import Tracer
from monitorables.debugger import Debugger

class Commander(Listener):

    def __init__(self):
        print("Self: %s" % str(self))
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


def main():
    cmd = Commander()
    factory = MicroserviceFactory()

    api = factory.create(MicroserviceEnum.API)
    tracer = Tracer(api, 'monitorables/%s_tracer.txt' % api)
    api.add_listener(tracer)
    debugger = Debugger(api, 'monitorables/%s_debugger.out' % api)
    api.add_listener(debugger)
    cmd.register(api)

    aas = factory.create(MicroserviceEnum.AAS)
    debugger = Debugger(aas, 'monitorables/%s_debugger.out' % aas)
    aas.add_listener(debugger)
    cmd.register(aas)
    """
    gqs = factory.create(MicroserviceEnum.GQS)
    cmd.register(gqs)

    valet = factory.create(MicroserviceEnum.VALET)
    cmd.register(valet)
    """

    while True:
        try:
            command = input(">>> ")
            if command == "exit":
                cmd.exit()
                break
            else:
                print(exec(command))
        except KeyboardInterrupt:
            print()
            break
        except (SyntaxError, NameError) as e:
            print(e)


if __name__ == "__main__":
    main()
    sys.exit(0)