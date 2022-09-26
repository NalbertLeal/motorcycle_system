from collections import namedtuple
import traceback
from typing import Callable, Optional

import kafka

from .util import create_topic_partitions

KafkaConsumer = namedtuple('KafkaConsumer', [
    'connection',
    'topic',
    'group'
])

def create_consumer(
        host: str,
        topic: str,
        group: str='some_group',
        partition_number: int=1
    ) -> KafkaConsumer:
    '''
    Create the KafkaConsumer object that store the conncetion 
    PARAMETERS:
        host: str
            The kafka broker host
        topic: str
            The kafka topics to listen
        group: str
            THe consumer group
        partition_number: int
            The number of partitions of the topic.
            DEFAULT = 1
    RETURNS: Tuple[Optional[KafkaProducer], Optional[str]]
        The KafkaProducer object
    '''
    create_topic_partitions(host, topic, partition_number)
    connection = kafka.KafkaConsumer(
        topic,
        bootstrap_servers=[host],
        group_id=group,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        max_partition_fetch_bytes=50000000
    )
    return KafkaConsumer(
        connection=connection,
        topic=topic,
        group=group,
    )

def listen(consumer: KafkaConsumer, callback: Callable) -> Optional[str]:
    '''
    Start to listen kafka using the consumer passed and call a function (passed
    by parameter) with the data received. If receive a message b'\0' from the
    broker then stop to listen the consumer.
    PARAMETERS:
        consumer: KafkaConsumer
            The consumer object.
        callback: Callable
            The function to pass the received data.
    RETURN: Optional[str]
        An optional error, if anything wrong occurs the return is an string
        with the error, otherwise return None
    '''
    try:
        for data in consumer.connection:
            if data.value == b'\0':
                print('STOPING')
                return
            callback(data)
    except Exception as e:
        return 'error message: ' + str(e) + '\n' + traceback.format_exc()