import sqlite3
from flask import Flask, request, jsonify

from models.location import Location
from models.toilet import Toilet
from models.user import User
from services.toilet_finder import ToiletFinder
from database.db import init_db, get_all_toilets_from_db, seed_real_data, get_connection

app = Flask(__name__, static_url_path='', static_folder='.')

init_db()
seed_real_data()

@app.route("/")
def home():
    return app.send_static_file('home.html')


@app.route("/api/nearest", methods=["POST"])
def get_nearest():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "No data provided or invalid JSON body"}), 400

        lat = data.get("lat")
        lon = data.get("lon")

        if lat is None or lon is None:
            return jsonify({"error": "lat/lon required"}), 400

        try:
            lat = float(lat)
            lon = float(lon)
        except (TypeError, ValueError):
            return jsonify({"error": "lat/lon must be numeric values"}), 400

        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            return jsonify({"error": "lat/lon values out of range"}), 400

        current_location = Location(latitude=lat, longitude=lon, building_name="User")
        user = User(current_location=current_location, is_gps_enabled=True)

        toilets = get_all_toilets_from_db()
        if not toilets:
            return jsonify({"error": "No toilet data found"}), 500

        toilet_finder = ToiletFinder(all_toilets=toilets)
        top3 = toilet_finder.get_top3(user.get_location())

        result = []
        for toilet in top3:
            distance = toilet_finder.calculate_distance(toilet.location, user.get_location())
            result.append({
                "name": toilet.name,
                "floor": toilet.floor,
                "info": toilet.info,
                "lat": toilet.location.latitude,
                "lon": toilet.location.longitude,
                "image_filename": toilet.image_filename or "photo/hongnum.png",
                "distance_km": round(distance, 4),
                "average_rating": toilet.average_rating,
                "review_count": toilet.review_count,
                "map_link": f"routing.html?lat={toilet.location.latitude}&lon={toilet.location.longitude}&name={toilet.name}&distance={round(distance * 1000)}&duration={max(round(distance * 12), 1)}&label={toilet.info or ''}"
            })
        return jsonify(result)

    except sqlite3.Error as db_error:
        app.logger.exception("Database error while fetching nearest toilets")
        return jsonify({"error": "Database error", "detail": str(db_error)}), 500
    except Exception as ex:
        app.logger.exception("Unexpected server error")
        return jsonify({"error": "Server error", "detail": str(ex)}), 500

@app.route("/api/add_review", methods=["POST"])
def add_review():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"status": "error", "message": "Invalid JSON"}), 400
            
        toilet_name = data.get("name")
        rating = data.get("rating")
        
        if not toilet_name or not rating:
            return jsonify({"status": "error", "message": "ข้อมูลไม่ครบถ้วน"}), 400
            
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE toilets 
            SET total_stars = total_stars + ?, review_count = review_count + 1 
            WHERE name = ?
        """, (rating, toilet_name))

        if cursor.rowcount == 0:
            print(f"⚠️ หาห้องน้ำชื่อ '{toilet_name}' ไม่เจอในระบบ")
        else:
            print(f"✅ อัปเดตรีวิวให้ '{toilet_name}' สำเร็จ (Row count: {cursor.rowcount})")
            
        conn.commit()
        conn.close()
        
        return jsonify({"status": "success", "message": "บันทึกรีวิวสำเร็จ"}), 200
        
    except Exception as ex:
        app.logger.exception("Error adding review")
        return jsonify({"status": "error", "message": str(ex)}), 500

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5000)