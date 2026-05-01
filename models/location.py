class Location:
    def __init__(self, latitude: float, longitude: float, building_name: str):
        self._latitude = float(latitude)
        self._longitude = float(longitude)
        self._building_name = str(building_name)
        if not self.is_valid():
            raise ValueError(f"Invalid coordinates: ({latitude}, {longitude})")

    @property
    def latitude(self) -> float:
        return self._latitude

    @latitude.setter
    def latitude(self, value: float):
        value = float(value)
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = value

    @property
    def longitude(self) -> float:
        return self._longitude

    @longitude.setter
    def longitude(self, value: float):
        value = float(value)
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = value

    @property
    def building_name(self) -> str:
        return self._building_name

    @building_name.setter
    def building_name(self, value: str):
        self._building_name = str(value)

    def get_name(self) -> str:
        return self._building_name

    def is_valid(self) -> bool:
        return -90 <= self._latitude <= 90 and -180 <= self._longitude <= 180

    def to_tuple(self) -> tuple:
        return (self._latitude, self._longitude)

    def __repr__(self) -> str:
        return f"Location({self._latitude}, {self._longitude}, '{self._building_name}')"
