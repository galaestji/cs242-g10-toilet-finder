import math


class Toilet:
    def __init__(self, name: str, floor: int, info: str, location):
        self.name = name
        self.floor = floor
        self.info = info
        self.location = location

    def get_info(self) -> str:
        return self.info

    def distance_to(self, loc) -> float:
        return math.sqrt(
            (self.location.latitude - loc.latitude) ** 2 +
            (self.location.longitude - loc.longitude) ** 2
        )