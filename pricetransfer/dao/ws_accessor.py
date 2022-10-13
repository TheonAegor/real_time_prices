import asyncio
import json
import typing as tp
import uuid
from dataclasses import asdict

from aiohttp import web

from pricetransfer.dao.base_accessors import IBaseAccessor
from pricetransfer.dao.kafka_accessor import AsyncKafkaAccessor
from pricetransfer.dto.application_dto import Request
from pricetransfer.dto.protocol_dto import Event
from pricetransfer.service.event_handler.general_event_manager import (
    GeneralEventManager,
)


class WSConnectionNotFound(Exception):
    """Error for no connection."""


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
        self.logger.debug("WSAccessor start handling request")

        ws_response = web.WebSocketResponse()
        await ws_response.prepare(request)
        connection_id = str(uuid.uuid4())
        self._first_connection_id = connection_id
        self._connections[connection_id] = ws_response

        self.logger.debug("Before initial message")

        await self._general_event_manager.server_EM.handle_open(
            connection_id,
            self,
        )
        await asyncio.gather(
            self.read(connection_id),
            self.tell(connection_id),
        )
        await self.close(connection_id)
        return ws_response

    async def tell(self, user_id: uuid.uuid4):
        # TODO check user for having trading tool
        await self._general_event_manager.server_EM.handle_tell(
            user_id=user_id,
            ws_accessor=self,
            source_accessor=self._source_accessor,
        )

    async def close(self, connection_id: str):
        self.logger.debug("WS accessor !!!CLOSED!!!")
        try:
            connection = self._connections.pop(connection_id)
        except KeyError:
            return None
        else:
            await connection.close()

        return None

    async def push(self, connection_id: str, event: Event):
        json_data = json.dumps(asdict(event))
        await self._push(connection_id, json_data)

    async def read(self, connection_id: str):
        async for message in self._connections[connection_id]:
            self.logger.debug("WebSocket read")
            self.logger.debug(message)
            raw_event = json.loads(message.data)
            await self._general_event_manager.client_EM.handle_event(
                event=Event(
                    kind=raw_event["kind"],
                    payload=raw_event["payload"],
                ),
            )
            self.logger.debug("Read. Client Event handled")

    async def _push(self, connection_id: str, data_to_send: str):
        try:
            await self._connections[connection_id].send_str(data_to_send)
        except KeyError as err:
            raise WSConnectionNotFound(err)
        except ConnectionResetError as err:
            self._connections.pop(connection_id)
            raise err

    def _init(self):

        self.logger.debug("WS_ACCESSOR start creating!")

        self._source_accessor = AsyncKafkaAccessor

        self.logger.debug("Before GeneralEventManager creating")

        trading_tools = [
            "ticker_%.2d" % num for num in range(100)  # noqa: WPS323
        ]
        self._general_event_manager = GeneralEventManager(
            extra={"trading_tools": trading_tools},
        )

        self.logger.debug("GeneralEventManager created")

        self._connections: dict[str, tp.Any] = {}

        self.logger.debug("WS_ACCESSOR created!")
