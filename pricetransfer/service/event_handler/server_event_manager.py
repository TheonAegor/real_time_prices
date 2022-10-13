import typing

from pricetransfer.dto.kafka_dto import Share
from pricetransfer.dto.protocol_dto import Event, ServerEventKind

if typing.TYPE_CHECKING:
    from dao.ws_accessor import WSAccessor
    from pricetransfer.dao.kafka_accessor import AsyncKafkaAccessor

from pricetransfer.service.logger.logging_service import get_my_logger


class ServerEventManager(object):
    """Handle server Events."""

    def __init__(self, share: Share):
        self.logger = get_my_logger("ServerEventManager")
        self._share = share

        self.logger.info("ServerEventManager created")

    async def handle_open(self, user_id: str, ws_accessor: "WSAccessor"):
        await ws_accessor.push(
            user_id,
            event=Event(
                kind=ServerEventKind.INITIAL,
                payload={
                    "id": str(user_id),
                    "trading_tools": self._share.get("trading_tools", ""),
                },
            ),
        )

    async def handle_tell(
        self,
        user_id: str,
        ws_accessor: "WSAccessor",
        source_accessor: "AsyncKafkaAccessor",
    ):
        self.logger.info("Start telling prices")
        resume = True
        tt = self._share.get("trading_tool", "ticker_99")
        pgs = source_accessor(tt)
        await pgs.async_configure(tt, 0)
        while True:  # noqa: WPS457
            if not resume:
                tt = self._share.get("trading_tool", "ticker_99")
                pgs.async_reconfigure(tt, 0)
            resume = True
            self._share.update({"resume": True})
            while resume:
                msg = await pgs.get_msg()
                new_price = msg.value
                await ws_accessor.push(
                    user_id,
                    event=Event(
                        kind=ServerEventKind.TELL,
                        payload={
                            "new_price": new_price,
                            "trading_tool": tt,
                            "full_info": msg,
                        },
                    ),
                )
                resume = self._share.get("resume", True)
