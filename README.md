# python-spring-cloud-stream
Python Spring Cloud Stream is a Python package for building highly scalable event-driven microservices connected with shared messaging systems. The framework provides a flexible programming model built on already established and familiar Spring idioms and best practices, including support for persistent pub/sub semantics, consumer groups, and stateful partitions.

Python Spring Cloud Stream supports a variety of binder implementations and the following table includes the link to the GitHub projects.
- RabbitMQ
- Apache Kafka
- Kafka Streams
- Amazon Kinesis
- Google PubSub
- Solace PubSub+
- Azure Event Hubs
- Apache RocketMQ

# Apache Kafka
## Publish/read messages from the Kafka topic
#### Step1 Create callback function:
    def onMessage(message):
        # TODO implement this method
        #  For example
        print('New Message :', message)

#### Step2 Use Commander class as CLI
    cli = Commander()

#### Step3 Initail and register StreamSubscriber
Like SpringApplication, *spring.config.location* is used very early to determine which files have to be loaded, so they must be defined as an environment property (typically an OS environment variable, a system property, or a command-line argument).
    subscriber = StreamSubscriber(onMessage, '--spring.config.location=file:*{your-application.yml or your-application.properties}*')
    cli.register(subscriber)
## Configuration File
It is also possible to configure the your Kafka consumer by using either application.properties or application.yml
    spring:
    cloud:
        stream:
        bindings:
            input:
                destination:  *your-topic*
                content-type: application/json
        kafka:
            binder:
            zkNodes: *your-zookeeper-server*
            brokers: *your-kafka-server*

![Class Diagram](https://github.com/superoutput/python-spring-cloud-stream/blob/master/documents/python-spring-cloud-stream_class_diagram.png)
