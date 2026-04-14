class MapService:
    def __init__(self):
        self.map_url = ""

    def open_navigation(self, destination):
        self.map_url = self.create_map_link(destination)
        return self.map_url

    def calculate_distance(self, origin, destination):
        return ((origin.latitude - destination.latitude) ** 2 + (origin.longitude - destination.longitude) ** 2) ** 0.5

    def create_map_link(self, destination):
        return f"https://www.google.com/maps/search/?api=1&query={destination.latitude},{destination.longitude}"