import dataclasses

@dataclasses.dataclass
class ServerEventKind:
    INITIAL = 'initial'  # отправляется при установке соединения с клиентом, сообщает ему выданный id
    TELL = 'tell' # сообщает новые данные клиенту


@dataclasses.dataclass
class ClientEventKind:
    CONNECT = 'connect'  # отправляется в ответ на ServerEventKind.INITIAL, содержит данные о клиенте
    PING = 'ping'  # отправляется клиентом раз в n секунд, содержит данные о текущей геопозиции
    DISCONNECT = 'disconnect'  # отправляется клиентом при ручном отсоединении от сервиса