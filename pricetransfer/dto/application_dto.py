from aiohttp import web

from logging import Logger

class Application(web.Application):
    # store: "Store"
    logger: Logger


class Request(web.Request):
    user_id: str

    @property
    def app(self) -> "Application":
        return super().app  # type: ignore