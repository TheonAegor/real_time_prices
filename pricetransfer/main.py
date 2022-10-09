from aiohttp import web

def setup_routes(app: web.Application):
    from routes import setup_routes

    setup_routes(app)

def setup_app() -> web.Application:
    app = web.Application()
    setup_routes(app)
    return app

def main():
    app = setup_app()
    web.run_app(app)


if __name__=='__main__':
    main()