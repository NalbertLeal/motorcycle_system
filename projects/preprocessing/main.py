import sys

sys.path.append('../../libs/kafka_lib')

from src.kafka import consumer as pre_consumer
from kafka_lib import consumer as lib_consumer

sub = pre_consumer.create_preprocessing_consumer()
lib_consumer.listen(sub, pre_consumer.receive_image)