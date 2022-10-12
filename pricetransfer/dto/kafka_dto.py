change = {"kind": "change", "payload": {"id": "e6", "trading_tool": "ticker_13"}}

from pricetransfer.service.logger.logging_service import get_my_logger


class Share:
    def __init__(self, share: dict):
        self.logger = get_my_logger("Share")
        self._share = share
        self.logger.info("Share created")

    def update(self, new_objects: dict):
        self.logger.info(f"Share update, new_object={new_objects}")
        self._share.update(new_objects)

    def get(self, key, default):
        self.logger.info(f"Get {key} from Share")
        return self._share.get(key, default)
