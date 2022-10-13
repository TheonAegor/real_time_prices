from random import random
import time
import datetime
from json import dumps
import asyncio

from kafka import KafkaProducer

kafka_server = "broker:9092"


def get_price_generator():
    last_price = 0

    def _generate_movement():
        movement = -1 if random() < 0.5 else 1

        return movement

    def _generate_new():
        nonlocal last_price
        last_price += _generate_movement()
        return last_price

    return _generate_new


class KafkaProducerManager:
    def __init__(self):
        self._producer = KafkaProducer(
            bootstrap_servers=kafka_server,
            value_serializer=lambda x: dumps(x).encode("utf-8"),
        )
        from .topic_creator import topic_names

        self._topics = topic_names
        self._gen_of_gens = get_price_generator
        self._init()

    async def asyncproduce(self):
        await asyncio.gather(
            *[
                asyncio.create_task(self._producer.send(topic, value=gen()))
                for topic, gen in self._topics_and_gens
            ]
        )

    def produce(self):
        for topic, gen in self._topics_and_gens:
            self._producer.send(
                topic, value={"value": gen(), "time": str(datetime.datetime.now())}
            )

    def _make_topics_and_gens(self):
        self._topics_and_gens = [(topic, self._gen_of_gens()) for topic in self._topics]

    def _init(self):
        self._make_topics_and_gens()


class PriceProducerService:
    """Generates prices every 1 second for 100 trading tools."""

    def __init__(self, producer):
        self._producer = producer()
        self._timer = 1

    async def asyncexecute(self):
        # counter = 100
        while True:
            await self._producer.produce()
            print(f"produce 1 more")
            await asyncio.sleep(self._timer)
            # counter -= 1

    def execute(self):
        # counter = 100
        # while counter:
        while True:
            self._producer.produce()
            print(f"produce 1 more")
            time.sleep(self._timer)
            # counter -= 1


def main():
    pps = PriceProducerService(producer=KafkaProducerManager)

    # asyncio.run(pps.execute())
    pps.execute()
