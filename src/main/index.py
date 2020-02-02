from py4j.java_gateway import JavaGateway, java_import, get_field, CallbackServerParameters
from py4j.clientserver import ClientServer, JavaParameters, PythonParameters

gateway = JavaGateway(callback_server_parameters=CallbackServerParameters())
#gateway = ClientServer(java_parameters=JavaParameters(), python_parameters=PythonParameters())

java_import(gateway.jvm, 'io.hms.mda.stream.spring.python.*')

class PythonCallbackImpl(object):
    def __init__(self, execfunc):
        self.execfunc = execfunc
    def notify(self, obj):
        print('[PythonCallbackImpl] notified from Java')
        self.execfunc()
        return 'dummy return value'
    class Java:
        implements = ["io.hms.mda.stream.spring.python.PythonCallback"]

def simple_fun():
    print('[simple_fun] called')
    gateway.jvm.System.out.println("[simple_fun] Hello from python!")

# Test 1: Without threading
input('Ready to begin test 1')
python_callback = PythonCallbackImpl(simple_fun)
nothread_executor = gateway.jvm.Test(python_callback)
nothread_executor.runSynchronous()

# Test 2: With threading
input('Ready to begin test 2')
python_callback = PythonCallbackImpl(simple_fun)
nothread_executor = gateway.jvm.Test(python_callback)
nothread_executor.runAsynchronous()

#gateway.shutdown()