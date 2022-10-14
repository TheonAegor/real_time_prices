from aiohttp import web

from pricetransfer.dao.base_accessors import IBaseAccessor
from pricetransfer.dto.application_dto import Request
from pricetransfer.service.logger.logging_service import get_my_logger


class PriceTransferService(object):
    """Service for getting messages."""

    def __init__(self, accessor: IBaseAccessor, request: Request):
        self.logger = get_my_logger("PriceTransferService")
        self.logger.debug("PriceTransferService start creating")
        self.accessor = accessor(self.logger)
        self.request = request
        self.logger.debug("PriceTransferService created!")

    async def execute(self) -> web.WebSocketResponse:
        ret = await self.accessor.handle_request(self.request)
        return ret
