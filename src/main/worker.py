from threading import Thread, Condition, Lock

class Worker(Thread):

    def __init__(self, microservice):
        Thread.__init__(self)
        self.condition = Condition(Lock())
        self.alive = True
        self.pause = False
        self.microservice = microservice
        self.daemon = None
        # self.start()

    def run(self):
        #while self.alive:
        with self.condition:
            while self.pause:
                self.condition.wait()
            # try:
            #     self.microservice.start()
            # except Exception as e:
            #     print(e)
            # finally:
            #     self.microservice.stop()
            self.microservice.start()

    def pause(self):
        self.pause = True
        self.condition.acquire()

    def resume(self):
        self.resume = False
        self.condition.notify()
        self.condition.release()

    def stop(self):
        self.alive = False
        self.join()