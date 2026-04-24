from flask import Flask, request, jsonify

from models.location import Location
from models.toilet import Toilet
from models.user import User
from services.toilet_finder import ToiletFinder
from services.map_service import MapService 
from database.db import init_db, get_all_toilets_from_db, seed_real_data

app = Flask(__name__)

init_db()
seed_real_data()

@app.route("/")
def home():
    return "OK"


@app.route("/api/nearest", methods=["POST"])
def get_nearest():
    data = request.json

    # กัน error กรณีไม่มี data
    if not data:
        return jsonify({"error": "No data provided"}), 400

    lat = data.get("lat")
    lon = data.get("lon")

    # กัน error กรณีไม่มี lat/lon
    if lat is None or lon is None:
        return jsonify({"error": "lat/lon required"}), 400

#    print("LAT LON:", lat, lon)

    # user
    current_location = Location(latitude=lat, longitude=lon, building_name="User")
    user = User(current_location=current_location, is_gps_enabled=True)

    # load toilets
    toilets = get_all_toilets_from_db()
#    print("TOILETS COUNT:", len(toilets))

    # logic
    toilet_finder = ToiletFinder(all_toilets=toilets)
    top3 = toilet_finder.get_top3(user.get_location())
#    print("TOP3:", top3)

    # format response
    result = []
    for toilet in top3:
        result.append({
            "name": toilet.name,
            "floor": toilet.floor,
            "info": toilet.info,
            "lat": toilet.location.latitude,
            "lon": toilet.location.longitude,
            "map_link": f"https://www.google.com/maps?q={toilet.location.latitude},{toilet.location.longitude}"
        })

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5000)