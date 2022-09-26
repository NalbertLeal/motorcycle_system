from os import environ
import sys

sys.path.append('../../libs/kafka_lib')

from src.kafka import consumer as pre_consumer
from kafka_lib import consumer as lib_consumer

HOST = environ.get('HOST', 'localhost:9092')
TOPIC = environ.get('TOPIC', 'source')

sub = lib_consumer.create_consumer(HOST, TOPIC)
lib_consumer.listen(sub, pre_consumer.receive_image)