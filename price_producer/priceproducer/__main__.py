import logging

from .price_producer import main as produce_prices
from .topic_creator import main as create_topics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def main():
    create_topics()
    logger.info('Topics created')
    produce_prices()
    logger.info('All topics filled with 100 values')