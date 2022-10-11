import typing
from dataclasses import asdict

from pricetransfer.dto.protocol_dto import Event
from pricetransfer.dto.protocol_dto import ServerEventKind
from pricetransfer.dao.kafka_accessor import KafkaAccessor

if typing.TYPE_CHECKING:
    from dao.ws_accessor import WSAccessor

from pricetransfer.service.logger.logging_service import get_my_logger


class ServerEventManager:
    def __init__(self, share: dict):
        self.logger = get_my_logger("ServerEventManager")
        self._share = share
        self.logger.info("ServerEventManager created")

    async def handle_open(self, user_id: str, ws_accessor: "WSAccessor"):
        await ws_accessor.push(
            user_id,
            event=Event(
                kind=ServerEventKind.INITIAL,
                payload={"id": str(user_id)},
            ),
        )

    async def handle_tell(
        self,
        user_id: str,
        ws_accessor: "WSAccessor",
        source_accessor: "KafkaAccessor",
        trading_tool: str,
    ):
        self.logger.info("Start telling prices")
        while True:
            pgs = source_accessor(self._share.get("trading_tool", "ticker_99"))
            resume = True
            self._share["resume"] = True
            async for new_price in pgs.poll_data(resume):
                if not self._share.get("resume", True):
                    break
                await ws_accessor.push(
                    user_id,
                    event=Event(
                        kind=ServerEventKind.TELL,
                        payload={"new_price": new_price, "trading_tool": trading_tool},
                    ),
                )
