import json
import os

from aiokafka import AIOKafkaConsumer
from aiokafka import TopicPartition as AioTopicPartition

from pricetransfer.dao.base_accessors import ISourceAccessor
from pricetransfer.service.logger.logging_service import get_my_logger


class AsyncKafkaAccessor(ISourceAccessor):
    """помогает получить разными способами данные из разных топиков."""

    def __init__(self, topic: str = None):
        self.logger = get_my_logger("AsyncKafkaAccessor")
        self.logger.debug("Start creating AsyncKafkaAccessor")
        self._bootstrap_servers = os.getenv("KAFKA_CONNECT", "localhost:9092")
        self._start_offset = 0
        self._topic = topic
        self.is_configured = False
        self._init(topic)

    def async_reconfigure(self, topic, partition):
        self.logger.debug("async REconfigure started")
        self._tp = topic
        self._configure_topic_partition(topic, partition)
        # await self._start_consumer()
        self._set_from_start()
        self.logger.debug("AsyncKafka async configure finished")

    async def async_configure(self, topic: str, partition: int):
        self.logger.debug("AsyncKafka async configure started")
        self._tp = topic
        self._configure_topic_partition(topic, partition)
        await self._start_consumer()
        self._set_from_start()
        self.logger.debug("AsyncKafka async configure finished")

    async def get_msg(self):
        msg = await self._consumer.getone()
        return msg

    async def stop_consumer(self):
        await self._consumer.stop()

    async def _start_consumer(self):
        await self._consumer.start()

    def _set_from_start(self):
        self._consumer.seek(self._tp, self._start_offset)

    def _configure_topic_partition(self, topic: str, partition: int):
        self.logger.debug(
            "Partition configuration started: topic={0}, partition={1}".format(
                topic,
                partition,
            ),
        )
        self._tp = AioTopicPartition(topic, partition)
        self._consumer.assign([self._tp])
        self.logger.debug("Partition assigned")

    def _configure_kafka_consumer(self, topic: str) -> bool:
        self.logger.debug(
            "Kafka configuration: server:{0} topic:{1}".format(
                self._topic,
                self._bootstrap_servers,
            ),
        )
        if topic:
            self._consumer = AIOKafkaConsumer(
                bootstrap_servers=self._bootstrap_servers,
                value_deserializer=lambda msg: json.loads(msg.decode("utf-8")),
            )
            self.logger.debug("Consumer created")

            self.is_configured = True
            return True
        self.is_configured = False
        return False

    def _init(self, topic: str) -> None:
        self.logger.debug("KafkaAccessor created")
        self._configure_kafka_consumer(topic)
        self.logger.debug("KafkaAccessor configured")

    def _set_from_end(self):
        self._consumer.seek_to_end = self._tp
