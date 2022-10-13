import abc

from pricetransfer.dto import Request


class IBaseAccessor(abc.ABC):
    """Interface for all accessors."""

    class Meta(object):
        name = "base_accessor"

    def __init__(self, logger):
        self.logger = logger
        self.logger.info("IBaseaccessor start creating")
        self._init()

    @abc.abstractmethod
    def handle_request(self, request: "Request"):
        raise NotImplementedError

    @abc.abstractmethod
    def _init(self) -> None:
        raise NotImplementedError


class ISourceAccessor(abc.ABC):
    """Interface for source accessors (KafkaAccessor)."""

    class Meta(object):
        name = "base_accessor"

    def __init__(self, logger):
        self._init()
        self.logger = logger

    @abc.abstractmethod
    def _init(self) -> None:
        raise NotImplementedError
