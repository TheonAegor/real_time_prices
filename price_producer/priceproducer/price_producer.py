import asyncio
import datetime
import time
from json import dumps as json_dumps
from random import random

from kafka import KafkaProducer
from priceproducer.topic_creator import topic_names

kafka_server = "broker:9092"


def get_price_generator():
    """Generate function for price generating."""
    last_price = 0

    def _generate_movement():  # noqa: WPS430
        movement = -1 if random() < 0.5 else 1  # noqa: S311,WPS459

        return movement

    def _generate_new():  # noqa: WPS430
        nonlocal last_price  # noqa: WPS420
        last_price += _generate_movement()
        return last_price

    return _generate_new


# TODO заменить на aiokafka
class KafkaProducerManager(object):
    """Set up kafka producer and send msg to topics."""

    def __init__(self):
        self._producer = KafkaProducer(
            bootstrap_servers=kafka_server,
            value_serializer=lambda msg: json_dumps(msg).encode("utf-8"),
        )

        self._topics = topic_names
        self._gen_of_gens = get_price_generator
        self._init()

    async def asyncproduce(self):
        await asyncio.gather(
            *[
                asyncio.create_task(self._producer.send(topic, value=gen()))
                for topic, gen in self._topics_and_gens
            ],
        )

    def produce(self):
        for topic, gen in self._topics_and_gens:
            self._producer.send(
                topic,
                value={
                    "value": gen(), "time": str(datetime.datetime.now()),
                },
            )

    def _make_topics_and_gens(self):
        self._topics_and_gens = [
            (topic, self._gen_of_gens()) for topic in self._topics
        ]

    def _init(self):
        self._make_topics_and_gens()


class PriceProducerService(object):
    """Generates prices every 1 second for 100 trading tools."""

    def __init__(self, producer):
        self._producer = producer()
        self._range = 10000
        self._timer = 1

    async def asyncexecute(self):
        for _ in range(self._range):
            await self._producer.produce()
            await asyncio.sleep(self._timer)

    def execute(self):
        for _ in range(self._range):
            self._producer.produce()
            time.sleep(self._timer)


def main():
    """Set up and launches price producing."""
    pps = PriceProducerService(producer=KafkaProducerManager)

    pps.execute()
