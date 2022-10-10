import typing
from dataclasses import asdict

from dto.protocol_dto import Event
from dto.protocol_dto import ServerEventKind
from service.price_generator.price_generator_service import PriceGeneratorService

if typing.TYPE_CHECKING:
    from dao.ws_accessor import WSAccessor

class ServerEventManager:
    def __init__(self):
        pass

    async def handle_open(self, user_id: str, ws_accessor: "WSAccessor"):
        await ws_accessor.push(
            user_id,
            event=Event(
                kind=ServerEventKind.INITIAL,
                payload={
                    'id': str(user_id)
                },
            ),
        )

    async def handle_tell(self, user_id: str, ws_accessor: "WSAccessor", trading_tool: str):
        pgs = PriceGeneratorService()
        new_price = pgs.execute()
        await ws_accessor.push(
            user_id,
            event=Event(
                kind=ServerEventKind.TELL,
                payload={
                    "new_price": new_price,
                    "trading_tool": trading_tool
                }
            )
        )
        pass
