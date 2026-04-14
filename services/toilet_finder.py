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

    def calculate_distance(self, loc1, loc2):
        return ((loc1.latitude - loc2.latitude) ** 2 + (loc1.longitude - loc2.longitude) ** 2) ** 0.5