from models.location import Location
from models.toilet import Toilet
from models.user import User
from services.toilet_finder import ToiletFinder
from services.map_service import MapService


def main():
    print("Campus Toilet Finder - Skeleton Project")

    current_location = Location(latitude=18.8040, longitude=98.9503, building_name="Unknown")
    user = User(current_location=current_location, is_gps_enabled=True)

    toilets = [
        Toilet(name="Toilet A", floor=1, info="Free", location=Location(18.8045, 98.9508, "Building A")),
        Toilet(name="Toilet B", floor=2, info="Paid", location=Location(18.8050, 98.9512, "Building B")),
        Toilet(name="Toilet C", floor=1, info="Free", location=Location(18.8038, 98.9499, "Building C")),
    ]

    toilet_finder = ToiletFinder(all_toilets=toilets)
    map_service = MapService()

    print("Skeleton ready for development.")


if __name__ == "__main__":
    main()