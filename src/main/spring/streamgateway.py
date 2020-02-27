import subprocess
from py4j.java_gateway import JavaGateway, java_import, launch_gateway, get_field, CallbackServerParameters
import pathlib

class StreamGateway(object):
    def __init__(self, execfunc):
        self.execfunc = execfunc

    def notify(self, obj, message):
        # for key in message.__iter__():
        #     print(message.__getitem__(key))
        self.execfunc.onMessage(message)

        return "A Return Value"

    class Java:
        # Spring
        # implements = ["spring.cloud.stream.python.PythonCallback"]
        # Kafka Consumer
        implements = ["io.hms.mda.stream.PythonCallback"]

    def start(self, args):
        # print('For the directory of the script being run:\n', pathlib.Path(__file__).parent.absolute())
        # print('For the current working directory:\n', pathlib.Path().absolute())
        # print('Arguments length = ', len(args))
        # Spring Libs
        # gw_args = ['java', '-jar', str(pathlib.Path(__file__).parent.absolute())+'/lib/spring-cloud-stream-gateway-0.1.7.jar', '-noverify', '-XX:TieredStopAtLevel=1', '-Dspring.jmx.enabled=false']
        # KAFKA Consumer Libs
        gw_args = ['java', '-jar', str(pathlib.Path(__file__).parent.absolute())+'/lib/spring-cloud-stream-gateway-0.1.8.jar']
        # print(gw_args)
        gw_args.extend(args)
        # print(gw_args)
        # for arg in args:
        #     print('Arg: ', arg)

        # for output_line in run_command('java -jar ../resources/lib/spring-cloud-stream-gateway-0.1.7.jar --spring.config.location=file:../resources/application.yml'):
        for output_line in self.run_command(gw_args):
            print(output_line)
            if output_line == b'serverStarted\n':
                gateway = JavaGateway(callback_server_parameters=CallbackServerParameters())
                # listener = StreamGateway(gateway)
                gateway.entry_point.registerListener(self)
                # self.execfunc.postConstruct()
                break

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