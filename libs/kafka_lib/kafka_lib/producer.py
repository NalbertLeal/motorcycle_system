from collections import namedtuple
import traceback
from typing import List, Optional, Tuple

import kafka

from .util import create_topic_partitions

KafkaProducer = namedtuple('KafkaProducer', ['connection', 'topics'])

def create_producer(
        host: str,
        topic: List[str],
        partition_number: int=1
    ) -> KafkaProducer:
    '''
    Create a KafkaProducer element that store the kafka conncetion and the
    topics to send the messages
    PARAMETERS:
        host: str
            The kafka broker host
        topic: List[str]
            the topics to send the messages
    RETURNS: KafkaProducer
        The KafkaProducer object
    '''
    create_topic_partitions(host, topic, partition_number)
    connection = kafka.KafkaProducer(
        bootstrap_servers=host,
        max_request_size=50000000,
    )
    return KafkaProducer(
        connection=connection,
        topics=topic
    )

def send_to_producer(producer: KafkaProducer, message: bytes) -> Optional[str]:
    '''
    Send a bytes message to all topics of a KafkaProcucer
    PARAMETERS:
        producer: KafkaProducer
            The producer object that contains the connection with the kafka
            and the topics to send the message
        massage: bytes
            The bytes message to send
    RETURNS: Optional[str]
        An optional error, if anything wrong occurs the return is an string
        with the error, otherwise return None
    '''
    try:
        for topic in producer.topics:
            producer.connection.send(topic, message)
            producer.connection.flush()
    except Exception as e:
        return 'error message: ' + str(e) + '\n' + traceback.format_exc()