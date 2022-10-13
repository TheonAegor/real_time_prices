import logging

from priceproducer.price_producer import main as produce_prices
from priceproducer.topic_creator import main as create_topics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def main():
    """Create topics."""
    create_topics()
    logger.debug("Topics created")
    produce_prices()
    logger.debug("All topics filled with 100 values")
