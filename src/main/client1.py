from spring.streamsubscriber import StreamSubscriber
from monitorables.debugger import Debugger

def postConstruct():
    # TODO Connection is connected. You can override function postConstruct()."
    print("Ready")

def onMessage(message):
    print('New Message :', message)
    print(type(message))

if __name__ == "__main__":
    try:
        # Spring
        # subscriber = StreamSubscriber(onMessage, '--spring.config.location=file:../resources/application.yml', '--spring.kafka.consumer.auto-offset-reset=earliest')
        # Kafka Consumer
        subscriber = StreamSubscriber(onMessage, 'localhost:9092', 'test')
    except (SyntaxError, NameError) as e:
        print(e)