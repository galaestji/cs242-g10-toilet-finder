class User:
    def __init__(self, current_location, is_gps_enabled: bool):
        self.current_location = current_location
        self.is_gps_enabled = is_gps_enabled

    def get_location(self):
        return self.current_location

    def find_toilet(self):
        pass

    def open_map(self):
        pass