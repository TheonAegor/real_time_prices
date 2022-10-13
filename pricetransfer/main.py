from aiohttp import web

from pricetransfer.api.routes import setup_routes as api_routes


def setup_routes(app: web.Application):
    """Set up app routes."""
    api_routes(app)


def setup_app() -> web.Application:
    """Set up all app."""
    app = web.Application()
    setup_routes(app)
    return app


def main():
    """Call setup_app and runs app."""
    app = setup_app()
    web.run_app(app)


if __name__ == "__main__":
    main()
