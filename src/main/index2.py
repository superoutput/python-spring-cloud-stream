from py4j.java_gateway import JavaGateway, CallbackServerParameters

class PythonListener(object):
    def __init__(self, gateway):
        self.gateway = gateway

    def notify(self, obj, message):
        print("Notified by Java: ", message)
        print(obj)
        gateway.jvm.System.out.println("Hello from python!")

        return "A Return Value"

    class Java:
        implements = ["io.hms.mda.stream.spring.python.PythonCallback"]

if __name__ == "__main__":
    try:
        gateway = JavaGateway(callback_server_parameters=CallbackServerParameters())
        listener = PythonListener(gateway)
        gateway.entry_point.registerListener(listener)
        # gateway.entry_point.notifyAllListeners()
    except KeyboardInterrupt:
        print('Stop streaming')
        gateway.shutdown()
    except (SyntaxError, NameError) as e:
        print('Stop streaming')
        gateway.shutdown()
        print(e)