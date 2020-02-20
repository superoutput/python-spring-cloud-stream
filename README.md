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
Like SpringApplication, *spring.config.location* is used very early to determine which files mandatory to be loaded, so it must be defined as an environment property .

If *spring.config.location* contains directories (as opposed to files), they should end in / . Files specified in *spring.config.location* are used as-is, with no support for profile-specific variants, and are overridden by any profile-specific properties.

The second property, *spring.kafka.consumer.auto-offset-reset* ensures the new consumer group gets the messages we sent, because the container might start after the sends have completed.

    subscriber = StreamSubscriber(onMessage, '--spring.config.location=file:{your-application-config}', '--spring.kafka.consumer.auto-offset-reset=earliest')
    cli.register(subscriber)
    
## Configuration File
It is also possible to configure your Kafka consumer by using either *application.properties* or *application.yml*

    spring:
    cloud:
        stream:
        bindings:
            input:
                destination:  {your-topic}
                content-type: application/json
        kafka:
            binder:
            zkNodes: {your-zookeeper-server}
            brokers: {your-kafka-server}

![Class Diagram](https://github.com/superoutput/python-spring-cloud-stream/blob/master/documents/python-spring-cloud-stream_class_diagram.png)
