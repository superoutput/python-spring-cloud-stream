from monitor.listener import Listener

class Monitorable(Listener):
    def __init__(self, microservice):
        self._mode = "DEBUG"
        self._microservice = microservice

    def fire(self, thread):
        print("Monitorable.fire()")

    def listen(self, event):
        print("Monitorable.listen()")