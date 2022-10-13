from logging import Logger

from aiohttp import web


class Application(web.Application):
    """Application dto."""

    logger: Logger


class Request(web.Request):
    """Request dto."""

    user_id: str

    @property
    def app(self) -> "Application":
        return super().app  # type: ignore
