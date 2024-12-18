
from app.rmq.rmq import get_broker
from app.db.nosqldb import get_db


def consume_switches():
    
    message_broker = get_broker()

    def callback(ch, method, properties, body):
        body = body.decode('utf-8')

        print(f" [x] Received {body}")
        switch_payload = {}

        if body["type"] == "CALLING_SWITCH":
            switch_payload = {
                "switch_mac_address": body["switch_mac"],
                "status": body["switch_value"],
                "timestamp": body["timestamp"],
                "type": "call"
            }
        elif body["type"] == "WORKER_TAGGED_SWITCH":
            switch_payload = {
                "switch_mac_address": body["switch_mac"],
                "worker_mac_address": body["beacon_mac"],
                "status": body["switch_value"],
                "timestamp": body["timestamp"],
                "type": "worker"
            }


        message_broker.publish_message('emergency_calls_processed', switch_payload)

        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    message_broker.register_consumer('emergency_calls', callback)


def start_consuming():

    message_broker = get_broker()

    message_broker.start_consuming()


def main():
    consume_switches()
    start_consuming()    