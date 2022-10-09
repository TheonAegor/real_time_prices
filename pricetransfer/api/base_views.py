import typing
from aiohttp import web

from dto.application_dto import Request
from dto.application_dto import Application


class View(web.View):
    @property
    def request(self) -> Request:
        return super().request  # type: ignore

    @property
    def app(self) -> "Application":
        return self.request.app