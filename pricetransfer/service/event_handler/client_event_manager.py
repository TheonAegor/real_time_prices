import uuid
from pricetransfer.dto.protocol_dto import Event
from pricetransfer.dto.protocol_dto import ClientEventKind
from pricetransfer.dto.protocol_dto import User

from pricetransfer.service.logger.logging_service import get_my_logger


class ClientEventManager:
    """Elaborate event"""

    def __init__(self, share: dict) -> None:
        self.logger = get_my_logger("ClientEventManager")
        self._users: dict[str, User] = {}
        self._share: dict = share

    async def handle_event(self, event: Event) -> None:
        # TODO сделать проверку что нет id
        user_id = event.payload["id"]  # клиент всегда присылает поле id
        if event.kind == ClientEventKind.CONNECT:
            await self._on_connect(user_id, event.payload)
        elif event.kind == ClientEventKind.DISCONNECT:
            await self._on_disconnect(user_id)
        elif event.kind == ClientEventKind.CHANGE:
            await self._on_change(user_id, event.payload["trading_tool"])
        else:
            raise NotImplementedError(event.kind)

    async def _on_connect(self, id: uuid.uuid4, payload: dict):
        self.logger.info(f"user [{id}] connected")
        self._users[id] = User(id=id)

    async def _on_disconnect(self, id: uuid.uuid4):
        self._users.pop(id)
        self.logger.info(f"user [{id}] disconnected")

    async def _on_change(self, id: uuid.uuid4, trading_tool: str):
        self.logger.info(f"user [{id}] changed trading_tool")
        user = self._users[id]
        user.trading_tool = trading_tool
        self._share["resume"] = False
        self._share["trading_tool"] = trading_tool
