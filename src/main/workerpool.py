from queue import Queue
from worker import Worker

class WorkerPool:
    def __init__(self):
        #self._threads = Queue(maxsize=num_threads)
        self._count = 0
        self._threads = dict()

    def add(self, microservice):
        # print('WorkerPool.add_task() : size %s' % len(self._threads))
        # print('Worker index : %s'%self._count)
        self._threads[self._count] = Worker(microservice)
        self._threads[self._count].start()
        self._count+=1

    def pause(self, index):
        print("Pause: %s"%self._threads[index])
        self._threads[index].pause()

    def resume(self, index):
        print("Resume: %s"%self._threads[index])
        self._threads[index].resume()

    def stop(self, index):
        print("Stop: %s"%self._threads[index])
        self._threads[index].stop()
        del self._threads[index]

    def exit(self):
        print("Exit")
        for _, _thread in self._threads.items():
            _thread.stop()
            _thread.join()
        #break
        self._threads.clear()

    def map(self, func, args_list):
        for args in args_list:
            self.add(func, args)
        
    def run(self, num_threads):
        for i in range(num_threads):
            worker = Thread(target=self.acquire)
            worker.setDaemon(True)
            worker.start()

        for _, _thread in self._threads.items():
            _thread.join()

    def take_task(self):
        print('WorkerPool.take_task() : size %s' % len(self._threads))
        reusable = self._threads.get()
        self._threads.task_done()
        return reusable