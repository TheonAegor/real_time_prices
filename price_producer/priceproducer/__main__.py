import logging

from priceproducer.price_producer import main as produce_prices
from priceproducer.topic_creator import main as create_topics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def main():
    """Create topics and start producing prices."""
    create_topics()
    logger.info("Topics created")
    produce_prices()
    logger.info("All topics filled with 100 values")
