from .client_event_manager import ClientEventManager
from .server_event_manager import ServerEventManager


class GeneralEventManager:
    def __init__(self):
        self._share: dict = {'resume': True}
        self.client_EM = ClientEventManager(self._share)
        self.server_EM = ServerEventManager(self._share)

    def update(self, new_objects: dict):
        self._share.update(new_objects)
