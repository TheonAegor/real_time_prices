from pricetransfer.api.views import ConnectView
from pricetransfer.dto.application_dto import Application


def setup_routes(app: Application):
    """Add route to router."""
    app.router.add_view("/connect", ConnectView)
