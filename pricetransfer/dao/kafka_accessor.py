import json
import os
from pricetransfer.dao.base_accessors import ISourceAccessor
from kafka import KafkaConsumer
from kafka import TopicPartition
from aiokafka import TopicPartition as AioTopicPartition
from aiokafka import AIOKafkaConsumer

from pricetransfer.service.logger.logging_service import get_my_logger


class AsyncKafkaAccessor(ISourceAccessor):
    """помогает получить разными способами данные из разных топиков"""

    def __init__(self, topic: str = None):
        self.logger = get_my_logger("AsyncKafkaAccessor")
        self.logger.info("Start creating AsyncKafkaAccessor")
        # self._bootstrap_server='broker:9092'
        self._bootstrap_servers = os.getenv("KAFKA_CONNECT", "localhost:9092")
        self._start_offset = 0
        self._topic = topic
        self.is_configured = False
        self._init(topic)

    @property
    def topic(self):
        return self._topic

    @topic.setter
    def topic(self, topic: str) -> str:
        self._topic = topic
        self._configure_kafka_consumer(topic)
        return self._topic

    async def async_configure(self):
        self.logger.info("AsyncKafka async configure started")
        await self.start_consumer()
        self._set_from_start()
        self.logger.info("AsyncKafka async configure finished")

    async def get_msg(self):
        self.logger.info(f"Start polling data from Kafka topic {self._topic}")
        msg = await self._consumer.getone()
        return msg 

    async def poll_data(self, resume):
        # self.logger.info(f"Start polling data from Kafka topic {self._topic}")
        # msg = await self._consumer.getone()
        # return msg 
        # try:
        async for msg in self._consumer:
            # self.logger.debug(f"msg = {msg}")
            if not resume:
                self.logger.info(f"STOP, DO NOT RESUME!")
                break
            self._last_offset = msg.offset
            yield msg
        # finally:
        #     await self._consumer.stop()

    async def start_consumer(self):
        await self._consumer.start()

    def _set_from_end(self):
        self._consumer.seek_to_end = self._tp

    def _set_from_start(self):
        self._consumer.seek(self._tp, self._start_offset)

    def _configure_kafka_consumer(self, topic: str) -> bool:
        self.logger.info(
            f"Kafka configuration: server:{self._bootstrap_servers} topic:{self._topic}"
        )
        if topic:
            self._consumer = AIOKafkaConsumer(
                bootstrap_servers=self._bootstrap_servers,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            )
            self.logger.info("Consumer created")

            self._tp = AioTopicPartition(topic, 0)
            self._consumer.assign([self._tp])

            self.logger.info("Partition assigned")

            # self._consumer.seek_to_beginning = self._tp
            # self._last_offset = self._consumer.position(self._tp)
            # self.logger.info(f"Last offset is {self._last_offset}")
            # self._set_from_start()
            # self.logger.info("Seeked to beginings")

            # if self._consumer.bootstrap_connected():
            self.is_configured = True
            return True
        self.is_configured = False
        return False

    def _init(self, topic: str) -> None:
        self.logger.info("KafkaAccessor created")
        self._configure_kafka_consumer(topic)
        self.logger.info("KafkaAccessor configured")


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
            self.logger.debug(f"msg = {msg}")
            if not resume:
                self.logger.info(f"STOP, DO NOT RESUME!")
                break
            yield msg

    def _set_from_end(self):
        self._consumer.seek_to_end = self._tp

    def _set_from_start(self):
        self._consumer.seek_to_beginning(self._tp)

    def _configure_kafka_consumer(self, topic: str) -> bool:
        self.logger.info(
            f"Kafka configuration: server:{self._bootstrap_servers} topic:{self._topic}"
        )
        if topic and not self.is_configured:
            self._consumer = KafkaConsumer(
                bootstrap_servers=self._bootstrap_servers,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            )
            self.logger.info("Consumer created")
            self._tp = TopicPartition(topic, 0)
            self._consumer.assign([self._tp])
            self.logger.info("Partition assigned")

            # self._consumer.seek_to_beginning = self._tp
            self._last_offset = self._consumer.position(self._tp)
            self.logger.info(f"Last offset is {self._last_offset}")
            self._set_from_start()
            self.logger.info("Seeked to beginings")

            # if self._consumer.bootstrap_connected():
            self.is_configured = True
            return True
        elif self.is_configured:
            self.logger.info("Consumer already configured")
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
