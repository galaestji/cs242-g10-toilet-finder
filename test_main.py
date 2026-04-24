from models.location import Location
from models.toilet import Toilet
from models.user import User
from services.toilet_finder import ToiletFinder
from services.map_service import MapService 
from database.db import init_db, get_all_toilets_from_db , seed_real_data

def main():
    print("Campus Toilet Finder - Systems Active")
 

 #--------------- มีการแก้ไขตรงนี้จ้า แก้สูตรนิดหน่อย ละก็แก้วิธีแสดงผลจร้า
    init_db()
    seed_real_data() 
    toilets = get_all_toilets_from_db()

    current_location = Location(latitude=18.8040, longitude=98.9503, building_name="Current Location")
    user = User(current_location=current_location, is_gps_enabled=True)

    toilet_finder = ToiletFinder(all_toilets=toilets)
    top3_toilets = toilet_finder.get_top3(user.get_location())

    print(f"\nพบห้องน้ำใกล้คุณ {len(top3_toilets)} อันดับ:")
    for i, toilet in enumerate(top3_toilets, 1):
        dist = toilet_finder.calculate_distance(user.get_location(), toilet.location)
        print(f"{i}. {toilet.name} - ชั้น {toilet.floor} ({toilet.info}) ระยะทาง: {dist:.4f} กม.")

#------------------------------------------------------------------
if __name__ == "__main__":
    main()