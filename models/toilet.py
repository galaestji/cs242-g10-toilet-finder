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
        R = 6371.0
        lat1, lon1 = math.radians(self.location.latitude), math.radians(self.location.longitude)
        lat2, lon2 = math.radians(loc.latitude), math.radians(loc.longitude)
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c