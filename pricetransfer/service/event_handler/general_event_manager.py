from .client_event_manager import ClientEventManager
from .server_event_manager import ServerEventManager
from pricetransfer.dto.kafka_dto import Share

from pricetransfer.service.logger.logging_service import get_my_logger


class GeneralEventManager:
    def __init__(self):
        self.logger = get_my_logger("GeneralEventManager")
        self.logger.info("GeneralEventManager start creating!")
        self._share: Share = Share({"resume": True})
        self.client_EM = ClientEventManager(self._share)
        self.server_EM = ServerEventManager(self._share)
        self.logger.info("GeneralEventManager created!")

    @property
    def topic(self):
        return self._share.get("topic", "ticker_01")

    @topic.setter
    def topic(self, topic):
        self._share["topic"] = topic
        return self._share.get("topic", "ticker_01")

    def update(self, new_objects: dict):
        self._share.update(new_objects)
