"""
@author : "Savage Lasa"
@copyright : "Copyright 2020, The Python Spring Cloud Stream Project"
@license : "GPL"
@version : "1.0.1"
@maintainer : "Savage Lasa"
@email : "superoutput@gmail.com"
@status : "Production"
"""

import sys
from py4j.java_gateway import JavaGateway, java_import, get_field, CallbackServerParameters
from py4j.clientserver import ClientServer, JavaParameters, PythonParameters

gateway = JavaGateway(callback_server_parameters=CallbackServerParameters())
#gateway = ClientServer(java_parameters=JavaParameters(), python_parameters=PythonParameters())

java_import(gateway.jvm, 'io.hms.mda.stream.spring.python.*')

class PythonCallbackImpl(object):
    def __init__(self, execfunc):
        self.execfunc = execfunc
    def notify(self, obj, event):
        print('[PythonCallbackImpl] notified from Java', event)
        self.execfunc()
        return 'dummy return value'
    class Java:
        implements = ["io.hms.mda.stream.spring.python.PythonCallback"]

def simple_fun():
    print('[simple_fun] called')
    gateway.jvm.System.out.println("[simple_fun] Hello from python!")


def main():
    print('Start streaming...')
    while True:

        try:
            command = input("> ")
            print('Command: ', command)
            if command == "exit":
                print('Stop streaming')
                gateway.shutdown()
                break
            elif command == "sync":
                python_callback = PythonCallbackImpl(simple_fun)
                nothread_executor = gateway.jvm.App(python_callback)
                nothread_executor.runSynchronous()
            elif command == "async":
                python_callback = PythonCallbackImpl(simple_fun)
                nothread_executor = gateway.jvm.App(python_callback)
                nothread_executor.runAsynchronous()
            else:
                print(exec(command))
        except KeyboardInterrupt:
            print('Stop streaming')
            gateway.shutdown()
            break
        except (SyntaxError, NameError) as e:
            print('Stop streaming')
            gateway.shutdown()
            print(e)

if __name__ == "__main__":
    main()
    sys.exit()