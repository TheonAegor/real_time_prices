import json
import os
from pricetransfer.dao.base_accessors import ISourceAccessor
from kafka import KafkaConsumer
from kafka import TopicPartition

from pricetransfer.service.logger.logging_service import get_my_logger


class KafkaAccessor(ISourceAccessor):
    """помогает получить разными способами данные из разных топиков"""

    def __init__(self, topic: str = None):
        # self._bootstrap_server='broker:9092'
        self._bootstrap_servers = os.getenv("KAFKA_CONNECT", "localhost:9092")
        self._topic = topic
        self.is_configured = False
        self.logger = get_my_logger("KafkaAccessor")
        self._init(topic)

    @property
    def topic(self):
        return self._topic

    @topic.setter
    def topic(self, topic: str) -> str:
        self._topic = topic
        self._configure_kafka_consumer(topic)
        return self._topic

    async def poll_data(self, resume: bool):
        self.logger.info(f"Start polling data from Kafka topic {self._topic}")
        for msg in self._consumer:
            if not resume:
                break
            await msg
            yield msg

    def _set_from_end(self):
        self._consumer.seek_to_end = self._tp

    def _set_from_start(self):
        self._consumer.seek_to_beginning(self._tp)

    def _configure_kafka_consumer(self, topic: str) -> bool:
        if topic and not self.is_configured:
            self._consumer = KafkaConsumer(
                bootstrap_servers=self._bootstrap_servers,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            )
            self._tp = TopicPartition(topic, 0)
            self._consumer.assign([self._tp])

            self._consumer.seek_to_beginning = self._tp
            self._last_offset = self._consumer.position(self._tp)
            self._set_from_start()

            # if self._consumer.bootstrap_connected():
            self.is_configured = True
            return True
        elif self.is_configured:
            self._consumer.assign()
            return True
        self.is_configured = False
        return False

    def _init(self, topic: str) -> None:
        self.logger.info("KafkaAccessor created")
        self._configure_kafka_consumer(topic)
        self.logger.info("KafkaAccessor configured")


# if __name__=='__main__':
#     ka = KafkaAccessor('ticker_01')
