import typing
from dataclasses import asdict

from pricetransfer.dto.protocol_dto import Event
from pricetransfer.dto.protocol_dto import ServerEventKind
from pricetransfer.dto.kafka_dto import Share

if typing.TYPE_CHECKING:
    from dao.ws_accessor import WSAccessor
    from pricetransfer.dao.kafka_accessor import KafkaAccessor
    from pricetransfer.dao.kafka_accessor import AsyncKafkaAccessor

from pricetransfer.service.logger.logging_service import get_my_logger


class ServerEventManager:
    def __init__(self, share: Share):
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
        source_accessor: "AsyncKafkaAccessor",
    ):
        self.logger.info("Start telling prices")
        resume = True
        tt = self._share.get("trading_tool", "ticker_99")
        pgs = source_accessor(tt)
        await pgs.async_configure(tt, 0)
        while True:
            if not resume:
                tt = self._share.get("trading_tool", "ticker_99")
                self.logger.info(
                    f"Need to reconfigure for topic {tt}, {str(self._share)}"
                )
                # pgs.stop_consumer()
                pgs.async_reconfigure(tt, 0)
            resume = True
            self.logger.info(f"Creating new source accessor in SEM with topic={tt}")
            self._share.update({"resume": True})
            while resume:
                new_price = await pgs.get_msg()
                await ws_accessor.push(
                    user_id,
                    event=Event(
                        kind=ServerEventKind.TELL,
                        payload={"new_price": new_price, "trading_tool": tt},
                    ),
                )
                resume = self._share.get("resume", True)

            # async for new_price in pgs.poll_data(resume):
            #     # self.logger.info("Get data from poll_data")
            #     if not self._share.get("resume", True):
            #         self.logger.info("STOP RESUME")
            #         break
            #     await ws_accessor.push(
            #         user_id,
            #         event=Event(
            #             kind=ServerEventKind.TELL,
            #             payload={"new_price": new_price, "trading_tool": tt},
            #         ),
            #     )
