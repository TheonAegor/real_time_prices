import typing as tp
import uuid

from aiohttp import web
from dao.base_accessors import IBaseAccessor
from dto.application_dto import Request


class WSAccessor(IBaseAccessor):
    """Handle change protocol to wss."""

    class Meta(object):
        """Doc."""

        name = 'ws'

    async def handle_request(
        self,
        request: 'Request',
    ) -> "web.WebSocketResponse":
        """Do all the work.

        Args:
            request: запрос

        Returns:
            web.WebsocketResponse
        """
        ws_response = web.WebSocketResponse()
        await ws_response.prepare(request)
        connection_id = str(uuid.uuid4())
        self._connections[connection_id] = ws_response
        await self._connections[connection_id].send_str('hello')
        await self.read(connection_id)
        await self.close(connection_id)
        return ws_response

    
    async def close(self, connection_id: str):
        try:
            connection = self._connections.pop(connection_id)
            await connection.close()
        except KeyError:
            return None

        # await self.store.geo.handle_close(str(connection_id))
        return None

    async def push(self, connection_id: str, event: Event):
        json_data = json.dumps(asdict(event))
        await self._push(connection_id, json_data)

    async def read(self, connection_id: str):
        async for message in self._connections[connection_id]:
            self.logger.info(message)

            # await self.push(connection_id, Event("add", {"message": message}))
            # self._refresh_timeout(connection_id)
            # raw_event = json.loads(message.data)
            # await self.store.geo.handle_event(event=Event(
            #     kind=raw_event['kind'],
            #     payload=raw_event['payload'],
            # ))

    def _init(self):
        self._connections: dict[str, tp.Any] = {}
