class Location:
    def __init__(self, latitude: float, longitude: float, building_name: str):
        self.latitude = latitude
        self.longitude = longitude
        self.building_name = building_name

    def get_name(self):
        return self.building_name