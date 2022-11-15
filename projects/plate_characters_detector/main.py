import os
import sys
sys.path.append('../libs/image_processing_lib')
sys.path.append('../libs/kafka_lib')
sys.path.append('../libs/mongodb_lib')
sys.path.append('../utils/protobuf/py/')

from kafka_lib import consumer as lib_consumer

from src.kafka import consumer as service_consumer

KAFKA_HOST = os.environ.get('KAFKA_HOST', default='localhost:9092')
KAFKA_CONSUMER_TOPIC = os.environ.get('KAFKA_CONSUMER_TOPIC', default='plates')
KAFKA_CONSUMER_PARTITIONS = int(os.environ.get('KAFKA_CONSUMER_PARTITIONS', default='1'))

sub = lib_consumer.create_consumer(
    KAFKA_HOST,
    KAFKA_CONSUMER_TOPIC,
    'chars_detector',
    KAFKA_CONSUMER_PARTITIONS
)
lib_consumer.listen(sub, service_consumer.receive_image)