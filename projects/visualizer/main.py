import sys
sys.path.append('../../libs/image_processing_lib')
sys.path.append('../../libs/kafka_lib')
sys.path.append('../../utils/protobuf/py/')

import os

from kafka_lib import consumer as kafka_lib_consumer

from src import consumer as src_consumer

KAFKA_HOST = os.environ.get('KAFKA_HOST', default='localhost:9092')
# KAFKA_CONSUMER_TOPIC = os.environ.get('KAFKA_CONSUMER_TOPIC', default='motorcycles')
KAFKA_CONSUMER_TOPIC = os.environ.get('KAFKA_CONSUMER_TOPIC', default='plates')
KAFKA_CONSUMER_PARTITIONS = int(os.environ.get('KAFKA_CONSUMER_PARTITIONS', default='1'))

consumer = kafka_lib_consumer.create_consumer(
    KAFKA_HOST,
    KAFKA_CONSUMER_TOPIC,
    'visualizer',
    KAFKA_CONSUMER_PARTITIONS
)

kafka_lib_consumer.listen(consumer, src_consumer.consume_frames)