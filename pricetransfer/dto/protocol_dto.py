import dataclasses

@dataclasses.dataclass
class Event:
    kind: str
    payload: dict
    # trading_tool - имя торгового инструмента

@dataclasses.dataclass
class ServerEventKind:
    INITIAL = 'initial'  # отправляется при установке соединения с клиентом, сообщает ему выданный id
    TELL = 'tell' # сообщает новые цены клиенту


@dataclasses.dataclass
class ClientEventKind:
    CONNECT = 'connect'  # отправляется в ответ на ServerEventKind.INITIAL, содержит данные о клиенте
    CHANGE = 'change' # отправляется когда клиент меняет тип данных
    DISCONNECT = 'disconnect'  # отправляется клиентом при ручном отсоединении от сервиса

@dataclasses.dataclass
class User:
    id: str
    trading_tool: str = None