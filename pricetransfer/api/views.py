from aiohttp import web

from pricetransfer.api.base_views import View
from pricetransfer.dao.ws_accessor import WSAccessor
from pricetransfer.service.logger.logging_service import get_my_logger
from pricetransfer.service.price_transfer.price_transfer_service import (
    PriceTransferService,
)

logger = get_my_logger("API")


class ConnectView(View):
    """Changes protocol for wss."""

    async def get(self) -> web.WebSocketResponse:
        logger.debug("get")
        price_service = PriceTransferService(
            accessor=WSAccessor,
            request=self.request,
        )
        ws = await price_service.execute()
        return ws
