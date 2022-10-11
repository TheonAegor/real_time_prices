from aiohttp import web
from pricetransfer.service.logger.logging_service import get_my_logger
from pricetransfer.dao.base_accessors import IBaseAccessor
from pricetransfer.dto.application_dto import Request


class PriceTransferService:
    def __init__(self, accessor: IBaseAccessor, request: Request):
        self.logger = get_my_logger('PriceTransferService')
        self.accessor = accessor(self.logger)
        self.request = request

    async def execute(self) -> web.WebSocketResponse:
        ret = await self.accessor.handle_request(self.request)
        return ret