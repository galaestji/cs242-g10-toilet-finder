import math

class ToiletFinder:
    def __init__(self, all_toilets: list):
        self.all_toilets = all_toilets

    def find_nearest(self, current_location):
        sorted_toilets = self.sort_by_distance(current_location)
        if sorted_toilets:
            return sorted_toilets[0]
        return None

    def get_top3(self, current_location):
        sorted_toilets = self.sort_by_distance(current_location)
        return sorted_toilets[:3]

    def sort_by_distance(self, current_location):
        return sorted(
            self.all_toilets,
            key=lambda toilet: self.calculate_distance(toilet.location, current_location)
        )
#------------ อันนี้แก้ให้สูตรมันตรงกันเฉยๆจร้า ไม่มีไรมากอ้วร ---------------------------------
    def calculate_distance(self, loc1, loc2):
        R = 6371.0 
        lat1, lon1 = math.radians(loc1.latitude), math.radians(loc1.longitude)
        lat2, lon2 = math.radians(loc2.latitude), math.radians(loc2.longitude)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

#--------------------------------------------------------------------------------