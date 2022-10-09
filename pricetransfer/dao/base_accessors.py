import abc
from dto.application_dto import Request

class IBaseAccessor(abc.ABC):
    """Interface for all accessors."""

    class Meta(object):
        name = 'base_accessor'

    def __init__(self, logger):
        self._init()
        self.logger = logger
    
    @abc.abstractmethod
    def handle_request(self, request: 'Request'):
        pass

    @abc.abstractmethod
    def _init(self) -> None:
        pass
