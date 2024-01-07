from enum import Enum

from kafka import KafkaProducer


class KafkaTopic(Enum):
    trending_videos = "trending_videos"


class KafkaHandler:

    def __init__(self, addr: str, port: int) -> None:
        self.addr = addr
        self.port = port

    def send_file_to_kafka(self, filename: str, topic_name: str) -> None:
        """
        This method sends the contents of a csv file to a kafka cluster.

        Parameters
        ----------
        filename: str
            The name of the file to send.
        topic_name: str
            The Kafka topic to send the file contents to.
        """
        producer = KafkaProducer(bootstrap_servers=f'{self.addr}:{self.port}')
        with open(filename, 'r', encoding='utf-8') as file:
            while line := file.readline():
                producer.send(topic_name, value=line.encode('utf-8'))
        producer.flush()

    def send_json_array_to_kafka(self, json_list: list, topic_name: str) -> None:
        """
        Sends a list of JSON objects to a specified Kafka topic.

        Parameters
        ----------
        json_list : list
            The list of JSON objects in dictionary format that are meant to be sent to the Kafka topic.
        topic_name : str
            The Kafka topic to be sent.

        Example
        -------
        >>> kafka_handler = KafkaHandler('localhost:9092')
        >>> json_array = [ {"key1": "value1", "key2": "value2"}, {"key3": "value3", "key4": "value4"}]
        >>> topic = "my_topic"
        >>> kafka_handler.send_json_array_to_kafka(json_array, topic)
        """
        producer = KafkaProducer(bootstrap_servers=f'{self.addr}:{self.port}')
        for json in json_list:
            producer.send(topic_name, value=json.encode('utf-8'))
        producer.flush()
