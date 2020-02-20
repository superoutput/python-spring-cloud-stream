import subprocess
from py4j.java_gateway import JavaGateway, java_import, launch_gateway, get_field, CallbackServerParameters

class StreamGateway(object):
    def __init__(self, execfunc):
        self.execfunc = execfunc

    def notify(self, obj, message):
        self.execfunc.onMessage(message)

        return "A Return Value"

    class Java:
        implements = ["io.hms.mda.stream.spring.python.PythonCallback"]

    def start(self, args):
        # print('Arguments length = ', len(args))
        gw_args = ['java', '-jar', '../resources/lib/spring-cloud-stream-gateway-0.1.1.jar', '-noverify', '-XX:TieredStopAtLevel=1', '-Dspring.jmx.enabled=false']
        # print(gw_args)
        gw_args.extend(args)
        # print(gw_args)
        # for arg in args:
        #     print('Arg: ', arg)

        # for output_line in run_command('java -jar ../resources/lib/spring-cloud-stream-gateway-0.1.1.jar --spring.config.location=file:../resources/application.yml'):
        for output_line in self.run_command(gw_args):
            # print(output_line)
            if output_line == b'serverStarted\n':
                gateway = JavaGateway(callback_server_parameters=CallbackServerParameters())
                # listener = StreamGateway(gateway)
                gateway.entry_point.registerListener(self)

        # self.run_command(gw_args)

    def run_command(self, command):
        p = subprocess.Popen(command,
            # shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        return iter(p.stdout.readline, b'')



def simple_fun():
    print('[simple_fun] called')
    gateway.jvm.System.out.println("[simple_fun] Hello from python!")