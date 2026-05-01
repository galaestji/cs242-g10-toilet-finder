import math


class ToiletFinder:
    def __init__(self, all_toilets: list):
        if not isinstance(all_toilets, list):
            raise TypeError("all_toilets must be a list")
        self._all_toilets = all_toilets

    @property
    def all_toilets(self) -> list:
        return self._all_toilets

    @all_toilets.setter
    def all_toilets(self, value: list):
        if not isinstance(value, list):
            raise TypeError("all_toilets must be a list")
        self._all_toilets = value

    def find_nearest(self, current_location):
        sorted_toilets = self.sort_by_distance(current_location)
        if sorted_toilets:
            return sorted_toilets[0]
        return None

    def get_top3(self, current_location):
        return self.sort_by_distance(current_location)[:3]

    def sort_by_distance(self, current_location):
        return sorted(
            self._all_toilets,
            key=lambda toilet: self.calculate_distance(toilet.location, current_location)
        )

    def calculate_distance(self, loc1, loc2) -> float:
        R = 6371.0
        lat1, lon1 = math.radians(loc1.latitude), math.radians(loc1.longitude)
        lat2, lon2 = math.radians(loc2.latitude), math.radians(loc2.longitude)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    def filter_by_max_distance(self, current_location, max_km: float) -> list:
        return [
            t for t in self._all_toilets
            if self.calculate_distance(t.location, current_location) <= max_km
        ]
