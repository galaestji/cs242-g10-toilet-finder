from services.toilet_finder import ToiletFinder
from services.map_service import MapService


class User:
    def __init__(self, current_location, is_gps_enabled: bool):
        self._current_location = current_location
        self._is_gps_enabled = bool(is_gps_enabled)

    @property
    def current_location(self):
        return self._current_location

    @current_location.setter
    def current_location(self, value):
        self._current_location = value

    @property
    def is_gps_enabled(self) -> bool:
        return self._is_gps_enabled

    @is_gps_enabled.setter
    def is_gps_enabled(self, value: bool):
        self._is_gps_enabled = bool(value)

    def get_location(self):
        if not self._is_gps_enabled:
            raise RuntimeError("GPS is disabled for this user")
        return self._current_location

    def find_toilet(self, toilets: list, top_n: int = 3) -> list:
        if not self._is_gps_enabled:
            raise RuntimeError("Cannot find toilet without GPS")
        if not toilets:
            return []
        finder = ToiletFinder(all_toilets=toilets)
        sorted_toilets = finder.sort_by_distance(self._current_location)
        return sorted_toilets[:top_n]

    def open_map(self, toilet) -> str:
        map_service = MapService()
        return map_service.open_navigation(toilet.location)

    def __repr__(self) -> str:
        return f"User(location={self._current_location}, gps={self._is_gps_enabled})"
