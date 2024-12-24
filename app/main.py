
from app.rmq.rmq import get_broker
from app.db.nosqldb import get_db
import json
from app.services.limiter import add_to_limiter


def consume_switches():
    
    message_broker = get_broker()

    def callback(ch, method, properties, body):
        body = json.loads(body.decode('utf-8'))

        cache_string = f"switch_{body['switch_mac']}"
        print(f" [x] Received {body}")
        switch_payload = {}

        if add_to_limiter(cache_string, body["timestamp"]):
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
                    "timestamp": body["timestamp"],
                    "type": "worker"
                }


            message_broker.publish('emergency_calls_processed', json.dumps(switch_payload))
        else:
            print("Duplicate packet")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    message_broker.register_consumer('emergency_calls', callback)


def start_consuming():

    message_broker = get_broker()

    message_broker.start_consuming()


def main():
    consume_switches()
    start_consuming()   

