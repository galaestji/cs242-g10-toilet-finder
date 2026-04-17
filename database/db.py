import sqlite3
from config import DATABASE_NAME
from models.location import Location
from models.toilet import Toilet


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS toilets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            floor INTEGER,
            info TEXT,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            building_name TEXT
        )
    """)

    conn.commit()
    conn.close()

#------------เพิ่มฟังก์ชันดึงห้องน้ำที่ใกล้ที่สุดจาก Db จร้า ไบโอมทำเอง -----------------------------------
def get_all_toilets_from_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, floor, info, latitude, longitude, building_name FROM toilets")
    rows = cursor.fetchall()
    conn.close()
    
    toilets = []
    for row in rows:
        name, floor, info, lat, lon, bldg = row
        location = Location(latitude=lat, longitude=lon, building_name=bldg)
        toilets.append(Toilet(name=name, floor=floor, info=info, location=location))
        
    return toilets


# ------------ อันนี้ข้อมูลหลอกจ้า อย่าไปเชื่อมาก ไม่มีอะไร เดี่ยวมาลบ หรือใครเกะกะก็ลบเลย ---------
def seed_dummy_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM toilets")
    if cursor.fetchone()[0] == 0:
        dummy_data = [
            ("Toilet A", 1, "Free", 18.8045, 98.9508, "Building A"),
            ("Toilet B", 2, "Paid", 18.8050, 98.9512, "Building B"),
            ("Toilet C", 1, "Free", 18.8038, 98.9499, "Building C"),
            ("Toilet D (Far)", 3, "Free", 18.8150, 98.9600, "Building D") # ตัวนี้ไกล จะต้องไม่ติด Top 3
        ]
        cursor.executemany("INSERT INTO toilets (name, floor, info, latitude, longitude, building_name) VALUES (?, ?, ?, ?, ?, ?)", dummy_data)
        conn.commit()
    conn.close()