from dto.application_dto import Application
from api.views import ConnectView

def setup_routes(app: Application):
    app.router.add_view("/connect", ConnectView)