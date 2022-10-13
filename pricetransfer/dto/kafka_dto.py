from pricetransfer.service.logger.logging_service import get_my_logger


class Share(object):
    """Let share dict between server and clien event managers."""

    def __init__(self, share: dict):
        self.logger = get_my_logger("Share")
        self._share = share
        self.logger.debug("Share created")

    def update(self, new_objects: dict):
        self.logger.debug("Share update, new_object={0}".format(new_objects))

        self._share.update(new_objects)

    def get(self, key, default):
        self.logger.debug("Get {0} from Share".format(key))

        return self._share.get(key, default)

    def __str__(self):
        """Return values from _share dict."""
        return " ".join(
            [
                "{0}={1}".format(share_key, share_value)
                for share_key, share_value in self._share.items()
            ],
        )
