import uuid
import json
import asyncio
import typing as tp
from dataclasses import asdict

from aiohttp import web
from pricetransfer.dao.base_accessors import IBaseAccessor
from pricetransfer.dto.application_dto import Request
from pricetransfer.dto.protocol_dto import Event
from pricetransfer.dto.protocol_dto import ServerEventKind

# from service.event_handler.client_event_manager import ClientEventManager
# from service.event_handler.server_event_manager import ServerEventManager
from pricetransfer.service.event_handler.general_event_manager import (
    GeneralEventManager,
)
from pricetransfer.dao.kafka_accessor import KafkaAccessor
from pricetransfer.dao.kafka_accessor import AsyncKafkaAccessor


class WSConnectionNotFound(Exception):
    pass


class WSAccessor(IBaseAccessor):
    """Handle change protocol to wss.

    Responsible for reading from and writing to ws.
    """

    class Meta(object):
        """Doc."""

        name = "ws"

    async def handle_request(
        self,
        request: "Request",
    ) -> "web.WebSocketResponse":
        """Do all the work.

        Args:
            request: запрос

        Returns:
            web.WebsocketResponse
        """
        self.logger.info("WSAccessor start handling request")
        ws_response = web.WebSocketResponse()
        await ws_response.prepare(request)
        connection_id = str(uuid.uuid4())
        self._connections[connection_id] = ws_response
        # await self.push(connection_id=connection_id, event=Event(ServerEventKind.INITIAL,{"id":connection_id}))
        self.logger.info("Before initial message")
        await self._general_event_manager.server_EM.handle_open(connection_id, self)
        await asyncio.gather(self.read(connection_id), self.tell(connection_id))
        await self.close(connection_id)
        return ws_response

    async def tell(self, user_id: uuid.uuid4):
        
        while True:
            await asyncio.sleep(1)
            # TODO check user for having trading tool
            await self._general_event_manager.server_EM.handle_tell(
                user_id=user_id,
                ws_accessor=self,
                source_accessor=self._source_accessor,
                trading_tool="ticker_01",
            )

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
            raw_event = json.loads(message.data)
            await self._general_event_manager.client_EM.handle_event(
                event=Event(
                    kind=raw_event["kind"],
                    payload=raw_event["payload"],
                )
            )

            # await self.push(connection_id, Event("add", {"message": message}))
            # self._refresh_timeout(connection_id)
            # raw_event = json.loads(message.data)
            # await self.store.geo.handle_event(event=Event(
            #     kind=raw_event['kind'],
            #     payload=raw_event['payload'],
            # ))

    async def _push(self, connection_id: str, data: str):
        try:
            await self._connections[connection_id].send_str(data)
        except KeyError:
            raise WSConnectionNotFound
        except ConnectionResetError:
            self._connections.pop(connection_id)
            raise

    def _init(self):
        self.logger.info("WS_ACCESSOR start creating!")
        self._general_event_manager = GeneralEventManager()
        self.logger.info("GeneralEventManager created")
        # self._client_event_manager = ClientEventManager()
        # self._server_event_manager = ServerEventManager()
        self._connections: dict[str, tp.Any] = {}
        self._source_accessor = AsyncKafkaAccessor
        self.logger.info("WS_ACCESSOR created!")
