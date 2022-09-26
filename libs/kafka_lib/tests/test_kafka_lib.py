import os
import time
import unittest
import threading

import kafka

from kafka_lib.util import is_broker_up, create_topic_partitions
from kafka_lib import producer
from kafka_lib import consumer

class TestKafkaLib(unittest.TestCase):
    def test_broker_up_function(self):
        HOST = os.environ.get('HOST', 'localhost:9092')

        ok = is_broker_up(HOST)
        self.assertTrue(ok)

    def test_create_topc_with_3_partitions(self):
        HOST = os.environ.get('HOST', 'localhost:9092')
        TOPIC = os.environ.get('TOPIC', 'test_create_topc_with_3_partitions')

        create_topic_partitions(HOST, TOPIC, 3)

        cons = kafka.KafkaConsumer(
            TOPIC,
            bootstrap_servers=HOST
        )
        partitions = cons.partitions_for_topic(TOPIC)
        topics_number = len(partitions)

        self.assertTrue(topics_number == 3)

    def test_produce_and_consume_msg(self):
        HOST = os.environ.get('HOST', '127.0.0.1:9092')
        TOPIC = os.environ.get('TOPIC', 'test_produce_and_consume_msg')

        prod = producer.create_producer(HOST, [TOPIC])
        producer.send_to_producer(prod, b'hello')
        producer.send_to_producer(prod, b'\0')

        def consumer_callback(data):
            if data.value == b'hello':
                self.assertTrue(True)
        cons = consumer.create_consumer(HOST, TOPIC)
        consumer.listen(cons, consumer_callback)