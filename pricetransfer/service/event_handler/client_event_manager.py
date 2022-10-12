from asyncio.log import logger
import uuid
import typing as tp
from pricetransfer.dto.protocol_dto import Event
from pricetransfer.dto.protocol_dto import ClientEventKind
from pricetransfer.dto.protocol_dto import User

from pricetransfer.service.logger.logging_service import get_my_logger

if tp.TYPE_CHECKING:
    from pricetransfer.dto.kafka_dto import Share


class ClientEventManager:
    """Elaborate event"""

    def __init__(self, share: "Share") -> None:
        self.logger = get_my_logger("ClientEventManager")
        self._users: dict[str, User] = {}
        self._share: "Share" = share

    async def handle_event(self, event: Event) -> None:
        # TODO сделать проверку что нет id
        user_id = event.payload["id"]  # клиент всегда присылает поле id
        if event.kind == ClientEventKind.CONNECT:
            await self._on_connect(user_id, event.payload)
        elif event.kind == ClientEventKind.DISCONNECT:
            await self._on_disconnect(user_id)
        elif event.kind == ClientEventKind.CHANGE:
            self.logger.info(f"!!!Change event!!!")
            self.logger.info(event)
            self.logger.info(event.payload)
            self.logger.info(user_id)
            await self._on_change(user_id, event.payload["trading_tool"])
        else:
            raise NotImplementedError(event.kind)

    async def _on_connect(self, id: uuid.uuid4, payload: dict):
        self.logger.info(f"user [{id}] connected")
        self._users[id] = User(id=id)
        self._first_user = self._users[id]

    async def _on_disconnect(self, id: uuid.uuid4):
        self._users.pop(id)
        self.logger.info(f"user [{id}] disconnected")

    async def _on_change(self, id: uuid.uuid4, trading_tool: str):
        self.logger.info(f"START ON CHANGE")
        # try:
        #     user = self._first_user
        #     self.logger.info("Get user")
        #     user.trading_tool = trading_tool
        #     self.logger.info(f"user [{id}] changed trading_tool to {trading_tool}")
        # except Exception as e:
        #     self.logger.info(f"Exception {e}")
        #     raise e
        self._share.update({"resume" : False})
        self._share.update({"trading_tool" : trading_tool})
