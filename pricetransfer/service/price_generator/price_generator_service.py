import random

class PriceGetterManager:
    """Подключается к источнику и отдает данные пока его не остановить."""
    def __init__(self, accssor):
        pass

    def get(self) -> int:
        return random.randint(0, 100)