class MapService:
    def __init__(self):
        self._map_url = ""

    @property
    def map_url(self) -> str:
        return self._map_url

    @map_url.setter
    def map_url(self, value: str):
        self._map_url = str(value)

    def open_navigation(self, destination) -> str:
        self._map_url = self.create_map_link(destination)
        return self._map_url

    def create_map_link(self, destination) -> str:
        return (
            f"https://www.google.com/maps/search/?api=1"
            f"&query={destination.latitude},{destination.longitude}"
        )

    def calculate_distance(self, origin, destination) -> float:
        dlat = origin.latitude - destination.latitude
        dlon = origin.longitude - destination.longitude
        return (dlat**2 + dlon**2) ** 0.5
