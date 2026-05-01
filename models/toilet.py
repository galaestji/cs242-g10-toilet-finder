import math


class Toilet:
    def __init__(self, name: str, floor: int, info: str, location,
                 image_filename: str = None, total_stars: int = 0, review_count: int = 0):
        if not name or not name.strip():
            raise ValueError("Toilet name cannot be empty")
        self._name = name.strip()
        self._floor = str(floor) if floor is not None else ""
        self._info = info or ""
        self._location = location
        self._image_filename = image_filename
        self._total_stars = max(0, int(total_stars))
        self._review_count = max(0, int(review_count))

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value or not value.strip():
            raise ValueError("Toilet name cannot be empty")
        self._name = value.strip()

    @property
    def floor(self) -> int:
        return self._floor

    @floor.setter
    def floor(self, value):
        self._floor = str(value) if value is not None else ""

    @property
    def info(self) -> str:
        return self._info

    @info.setter
    def info(self, value: str):
        self._info = value or ""

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def image_filename(self) -> str:
        return self._image_filename

    @image_filename.setter
    def image_filename(self, value: str):
        self._image_filename = value

    @property
    def total_stars(self) -> int:
        return self._total_stars

    @total_stars.setter
    def total_stars(self, value: int):
        if int(value) < 0:
            raise ValueError("total_stars cannot be negative")
        self._total_stars = int(value)

    @property
    def review_count(self) -> int:
        return self._review_count

    @review_count.setter
    def review_count(self, value: int):
        if int(value) < 0:
            raise ValueError("review_count cannot be negative")
        self._review_count = int(value)

    @property
    def average_rating(self) -> float:
        if self._review_count == 0:
            return 0.0
        return round(self._total_stars / self._review_count, 1)

    def get_info(self) -> str:
        return self._info

    def add_review(self, stars: int):
        if not (1 <= stars <= 5):
            raise ValueError("Rating must be between 1 and 5")
        self._total_stars += stars
        self._review_count += 1

    def distance_to(self, loc) -> float:
        R = 6371.0
        lat1 = math.radians(self._location.latitude)
        lon1 = math.radians(self._location.longitude)
        lat2 = math.radians(loc.latitude)
        lon2 = math.radians(loc.longitude)
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    def __repr__(self) -> str:
        return f"Toilet('{self._name}', floor={self._floor}, rating={self.average_rating})"
