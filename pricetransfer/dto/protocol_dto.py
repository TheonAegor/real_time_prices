import dataclasses


@dataclasses.dataclass
class Event:  # noqa: WPS306
    """Event structure."""

    kind: str
    payload: dict


@dataclasses.dataclass
class ServerEventKind:  # noqa: WPS306
    """Server event structure."""

    INITIAL = "initial"  # noqa: WPS115
    TELL = "tell"  # noqa: WPS115


@dataclasses.dataclass
class ClientEventKind:  # noqa: WPS306
    """Client event structure."""

    CONNECT = "connect"  # noqa: WPS115
    CHANGE = "change"  # noqa: WPS115
    DISCONNECT = "disconnect"  # noqa: WPS115


@dataclasses.dataclass
class User:  # noqa: WPS306
    """User object."""

    id: str
    trading_tool: str = None
