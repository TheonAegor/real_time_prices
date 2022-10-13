import logging

from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, UnknownTopicOrPartitionError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
kafka_server = "broker:9092"
admin_client = KafkaAdminClient(bootstrap_servers=kafka_server)
topic_names = ["ticker_%.2d" % num for num in range(100)]  # noqa: WPS323


def create_topics(topics):
    """Create and add topics to Kafka."""
    topic_list = []
    existing_topic_list = []
    for topic in topics:
        if topic not in existing_topic_list:
            logger.info("Topic : {0} added ".format(topic))
            topic_list.append(
                NewTopic(name=topic, num_partitions=1, replication_factor=1),
            )
        else:
            logger.info("Topic : {topic} already exist ")
    try:
        if topic_list:
            admin_client.create_topics(
                new_topics=topic_list,
                validate_only=False,
            )
            logger.info("Topic Created Successfully")
        else:
            logger.info("Topic Exist")
    except TopicAlreadyExistsError:
        logger.info("Topic Already Exist")
    except Exception as err:
        logger.info(err)


def delete_topics(topics: list):
    """Delete all topics."""
    try:
        admin_client.delete_topics(topics=topics)
    except UnknownTopicOrPartitionError:
        logger.info("Topic Doesn't Exist")
    except Exception as err:
        logger.info(err)
    else:
        logger.info("Topic Deleted Successfully")


def main():
    """Set up and start creating topics."""
    create_topics(topic_names)


if __name__ == "__main__":
    create_topics(topic_names)
