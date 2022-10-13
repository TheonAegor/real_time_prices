import typing as tp
import uuid

from pricetransfer.dto.protocol_dto import ClientEventKind, Event, User
from pricetransfer.service.logger.logging_service import get_my_logger

if tp.TYPE_CHECKING:
    from pricetransfer.dto.kafka_dto import Share


class ClientEventManager(object):
    """Elaborate event."""

    def __init__(self, share: "Share") -> None:
        self.logger = get_my_logger("ClientEventManager")
        self._users: dict[str, User] = {}
        self._share: "Share" = share

    async def handle_event(self, event: Event) -> None:
        # TODO сделать проверку что нет connection_id
        user_id = event.payload["connection_id"]
        if event.kind == ClientEventKind.CONNECT:
            await self._on_connect(user_id, event.payload)
        elif event.kind == ClientEventKind.DISCONNECT:
            await self._on_disconnect(user_id)
        elif event.kind == ClientEventKind.CHANGE:

            self.logger.info("!!!Change event!!!")
            self.logger.info(event)
            self.logger.info(event.payload)
            self.logger.info(user_id)

            await self._on_change(user_id, event.payload["trading_tool"])
        else:
            raise NotImplementedError(event.kind)

    async def _on_connect(self, connection_id: uuid.uuid4, payload: dict):
        self.logger.info("user [{0}] connected".format(connection_id))
        self._users[connection_id] = User(connection_id=connection_id)
        self._first_user = self._users[connection_id]

    async def _on_disconnect(self, connection_id: uuid.uuid4):
        self._users.pop(connection_id)
        self.logger.info("user [{0}] disconnected".format(connection_id))

    async def _on_change(self, connection_id: uuid.uuid4, trading_tool: str):
        user = self._users[connection_id]

        self.logger.info("User-{0} changed trading tool".format(user))

        self._share.update({"resume": False})
        self._share.update({"trading_tool": trading_tool})
