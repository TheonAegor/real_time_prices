from aiohttp import web

from api.base_views import View
from dao.ws_accessor import WSAccessor
from service.price_transfer.price_transfer_service import PriceTransferService
from service.logger.logging_service import get_my_logger

logger = get_my_logger('API')

class ConnectView(View):
    """Changes protocol for wss."""

    async def get(self) -> web.WebSocketResponse:
        logger.info('get')
        price_service = PriceTransferService(accessor=WSAccessor, request=self.request)
        ws = await price_service.execute()
        return ws
