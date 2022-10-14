from pricetransfer.dto.kafka_dto import Share
from pricetransfer.service.event_handler.client_event_manager import (
    ClientEventManager,
)
from pricetransfer.service.event_handler.server_event_manager import (
    ServerEventManager,
)
from pricetransfer.service.logger.logging_service import get_my_logger


class GeneralEventManager(object):
    """Create Client and Server event manager and share info between them."""

    def __init__(self, extra: dict = {}):  # noqa: B006,WPS404
        self.logger = get_my_logger("GeneralEventManager")

        self.logger.debug("GeneralEventManager start creating!")

        self._share: Share = Share({"resume": True, **extra})
        self.client_EM = ClientEventManager(self._share)
        self.server_EM = ServerEventManager(self._share)

        self.logger.debug("GeneralEventManager created!")

    @property
    def topic(self):
        return self._share.get("topic", "ticker_01")

    @topic.setter
    def topic(self, topic):
        self._share["topic"] = topic
        return self._share.get("topic", "ticker_01")

    def update(self, new_objects: dict):
        self._share.update(new_objects)
