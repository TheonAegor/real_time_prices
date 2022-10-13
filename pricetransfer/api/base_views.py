from aiohttp import web

from pricetransfer.dto.application_dto import Application, Request


class View(web.View):
    """Base view."""

    @property
    def request(self) -> Request:
        return super().request  # type: ignore

    @property
    def app(self) -> "Application":
        return self.request.app
