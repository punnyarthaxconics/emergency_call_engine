import os
import pika


class MessageBroker:
    def __init__(self, connection_string: str, exchange_name: str, exchange_type: str = 'direct',queues: list = []):
        print(f"Initializing Message Broker {connection_string}")
        self.connection_string = connection_string
        self.connection = pika.BlockingConnection(pika.URLParameters(connection_string))
        self.channel = self.connection.channel()

        # Check if connection is established

        if self.connection.is_open:
            print("Connection to RabbitMQ established")
        else:
            print("Connection to RabbitMQ failed")
            raise ConnectionError("Connection to RabbitMQ failed")
        self.exchange_name = exchange_name

        self.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

        for queue in queues:
            self.channel.queue_declare(queue=queue)
            self.channel.queue_bind(exchange=exchange_name, queue=queue, routing_key=queue)
        
    
    def publish(self, queue: str, message: str):
        self.channel.basic_publish(exchange=self.exchange_name, routing_key=queue, body=message)

    def register_consumer(self, queue: str, callback):
        
        self.channel.basic_consume(queue=queue, on_message_callback=callback,)

    def start_consuming(self):
        print("Consuming Initialized")
        self.channel.start_consuming()
        print("Consuming Started")
    
    def close(self):
        self.connection.close()

from dotenv import load_dotenv

load_dotenv(override=True)

# Initialize the message broker
connection_string = os.getenv('RABBITMQ_CONNECTION_STRING')
exchange_name = os.getenv('RABBITMQ_EXCHANGE_NAME')
queues = os.getenv('RABBITMQ_QUEUES').split(',')
exchange_type = os.getenv('RABBITMQ_EXCHANGE_TYPE')


message_broker = MessageBroker(connection_string, exchange_name, exchange_type, queues)

def get_broker():
    return message_broker



    

    
