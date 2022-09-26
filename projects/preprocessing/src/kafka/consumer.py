from os import environ

from kafka_lib import consumer as lib_consumer

def create_preprocessing_consumer():
    HOST = environ.get('HOST', 'localhost:9092')
    TOPIC = environ.get('TOPIC', 'source')

    return lib_consumer.create_consumer(HOST, TOPIC)

def receive_image(message: bytes):
    ...