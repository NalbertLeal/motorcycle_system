import kafka
import kafka.admin as kafkaAdm

def is_broker_up(host: str) -> bool:
    '''
    Indicate if the KafkaProducer has connection with the kafka broker
    PARAMETES:
        producer: KafkaProducer
            The producer to be verified if has conncetion
    RETUNS: bool
        True if has connection and false otherwise
    '''
    consumer = kafka.KafkaConsumer(
        group_id='test',
        bootstrap_servers=['localhost:9092']
    )
    topics = consumer.topics()
    if not topics: 
        return False
    return True

def create_topic_partitions(host: str, topic: str, partition_number: int):
    '''
    The topic may not be created and in some cases may be necessary create
    a diferente partition number to this topic instead the default number.
    This function create the topic with the desired partition number.
    PARAMETERS:
        host: str
            The kafka host
        topic: str
            The topic name
        partition_number: int
            The number of partitions of the topic
    '''
    adm_conn = kafka.KafkaAdminClient(bootstrap_servers=host)
    try:
        new_topic = kafkaAdm.NewTopic(
            name=topic,
            num_partitions=partition_number,
            replication_factor=1
        )
        adm_conn.create_topics(
            new_topics=[new_topic],
            validate_only=False
        )
    except:
        # topic alread created
        ...
    adm_conn.close()