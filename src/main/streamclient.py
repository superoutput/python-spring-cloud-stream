from streamsubscriber import StreamSubscriber
from commander import Commander
from monitorables.debugger import Debugger

def onMessage(message):
    print('New Message :', message)

if __name__ == "__main__":
    try:
        cmd = Commander()
        subscriber = StreamSubscriber(onMessage, '--spring.config.location=file:../resources/application.yml', '--spring.kafka.consumer.auto-offset-reset=earliest')
        # debugger = Debugger(subscriber, 'monitorables/%s_debugger.out' % subscriber)
        # subscriber.add_listener(debugger)
        cmd.register(subscriber)
    except KeyboardInterrupt:
        print('Stop streaming')
        gateway.shutdown()
    except (SyntaxError, NameError) as e:
        print('Stop streaming')
        gateway.shutdown()
        print(e)