import random

class PriceGeneratorService:
    def __init__(self):
        pass

    def execute(self) -> int:
        return random.randint(0, 100)