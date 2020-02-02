class Event(object):
    pass

class EventHandler(object):
    def __init__(self):
        self.callbacks = []

    def subscribe(self, listener):
        self.callbacks.append(listener.listen)

    def notify(self, **attrs):
        e = Event()
        e.source = self
        for k, v in attrs.items():
            setattr(e, k, v)
        for fn in self.callbacks:
            fn(e)