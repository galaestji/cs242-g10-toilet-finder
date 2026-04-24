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
            floor TEXT,
            info TEXT,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            building_name TEXT,
            is_disabled INTEGER NOT NULL DEFAULT 0     
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS toilet_images (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            toilet_id   INTEGER NOT NULL,
            image_filename TEXT NOT NULL,
            FOREIGN KEY (toilet_id) REFERENCES toilets(id)
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
""" 
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
"""

def seed_real_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM toilets")
    if cursor.fetchone()[0] == 0:
        TOILETS = [
            ("ห้องน้ำโรงอาหารกรีน",                    "1",       "ห้องน้ำหญิงอยู่ระหว่างการปรับปรุง",  14.07358, 100.60100, "โรงอาหารกรีน",           1),
            ("ห้องน้ำโรงอาหารกรีนดึก",                  "1",       "",                                   14.07397, 100.60121, "โรงอาหารกรีนดึก",         0),
            ("ห้องน้ำคนพิการ บร.1",                     "1",       "ห้องน้ำคนพิการ อยู่คนละจุด",         14.07271, 100.60185, "อาคารบรรยายรวม 1",        1),
            ("ห้องน้ำ บร.1",                            "1",       "",                                   14.07247, 100.60223, "อาคารบรรยายรวม 1",        0),
            ("ห้องน้ำอาคารเดือนบุนนาค",                  "1",       "",                                   14.07312, 100.60448, "อาคารเดือนบุนนาค",        0),
            ("ห้องน้ำ บร.2 ฝั่งที่จอดรถ",               "1,2",     "",                                   14.07340, 100.60605, "อาคารบรรยายรวม 2",        0),
            ("ห้องน้ำ บร.2 ฝั่งห้องกระจก",              "1",       "มีห้องน้ำคนพิการแยก",                14.07337, 100.60615, "อาคารบรรยายรวม 2",        1),
            ("ห้องน้ำ บร.3 ฝั่งน้ำพุ",                  "1",       "",                                   14.07260, 100.60666, "อาคารบรรยายรวม 3",        0),
            ("ห้องน้ำ บร.3 ฝั่งห้องเรียนด้านหลัง",      "1",       "ห้องน้ำคนพิการอยู่ข้างใน",           14.07239, 100.60590, "อาคารบรรยายรวม 3",        1),
            ("ห้องน้ำ บร.4 ด้านหลังติด บร.3",           "1,2,3",   "",                                   14.07274, 100.60788, "อาคารบรรยายรวม 4",        0),
            ("ห้องน้ำ บร.5 ฝั่งทางเข้าต่อกับทางเดิน",   "1,2,3,4,5","ห้องน้ำคนพิการอยู่ด้านใน",         14.07319, 100.60783, "อาคารบรรยายรวม 5",        1),
            ("ห้องน้ำ บร.5 ฝั่งด้านหลังศาลพระภูมิ",     "1,2,3,4,5","ห้องน้ำคนพิการอยู่ด้านใน",         14.07386, 100.60773, "อาคารบรรยายรวม 5",        1),
            ("ห้องน้ำ บร.5 ฝั่งประตูทางเข้าใหญ่",       "1,2,3,4,5","ห้องน้ำคนพิการอยู่ด้านใน",         14.07443, 100.60796, "อาคารบรรยายรวม 5",        1),
            ("ห้องน้ำ บร.5 ฝั่งลานเก้าอี้กว้าง",        "1,2,3,4,5","ห้องน้ำคนพิการอยู่ด้านใน",         14.07341, 100.60813, "อาคารบรรยายรวม 5",        1),
            ("ห้องน้ำศูนย์การเรียนรู้",                  "1,2,3,4", "ห้องน้ำคนพิการแยก",                 14.07164, 100.60313, "ศูนย์การเรียนรู้",         1),
            ("ห้องน้ำป๋วยฯ ฝั่งใกล้ทางออก",             "1",       "ห้องน้ำคนพิการแยก",                 14.07112, 100.60195, "หอสมุดป๋วย อึ๊งภากรณ์",   1),
            ("ห้องน้ำป๋วยฯ ฝั่งประตูทางเชื่อมไปศกร",   "2",       "",                                   14.07124, 100.60278, "หอสมุดป๋วย อึ๊งภากรณ์",   0),
            ("ห้องน้ำป๋วยฯ ฝั่ง co-learning",           "2",       "",                                   14.07132, 100.60223, "หอสมุดป๋วย อึ๊งภากรณ์",   0),
        ]
        cursor.executemany("""
            INSERT INTO toilets (name, floor, info, latitude, longitude, building_name, is_disabled)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, TOILETS)

        IMAGES = [
    # โรงอาหารกรีน (id=1)
    (1, "photo/toilets/green_M.jpg"),
    (1, "photo/toilets/green_W.jpg"),
    # โรงอาหารกรีนดึก (id=2)
    (2, "photo/toilets/nightgreen_M.jpg"),
    (2, "photo/toilets/nightgreen_W.jpg"),
    # อาคารเดือนบุนนาค (id=3)
    (3, "photo/toilets/Duan Bunnag_M.jpg"),
    (3, "photo/toilets/Duan Bunnag_W.jpg"),
    # บร.1 คนพิการ (id=4)
    (4, "photo/toilets/LC1-1_M.jpg"),
    (4, "photo/toilets/LC1-1_W.jpg"),
    # บร.1 (id=5)
    (5, "photo/toilets/LC1-2_M.jpg"),
    (5, "photo/toilets/LC1-2_W.jpg"),
    # บร.2 ฝั่งที่จอดรถ (id=6)
    (6, "photo/toilets/LC2-1_M.jpg"),
    (6, "photo/toilets/LC2-1_W.jpg"),
    # บร.2 ฝั่งกระจก (id=7)
    (7, "photo/toilets/LC2-2_M.jpg"),
    (7, "photo/toilets/LC2-2_W.jpg"),
    (7, "photo/toilets/LC2-2_D.jpg"),
    (7, "photo/toilets/LC2-2_All.jpg"),
    # บร.3 ฝั่งน้ำพุ (id=8)
    (8, "photo/toilets/LC3-1_M.jpg"),
    (8, "photo/toilets/LC3-1_M2.jpg"),
    (8, "photo/toilets/LC3-1_W.jpg"),
    # บร.3 ฝั่งห้องเรียน (id=9)
    (9, "photo/toilets/LC3-2_M.jpg"),
    (9, "photo/toilets/LC3-2_M2.jpg"),
    (9, "photo/toilets/LC3-2_W.jpg"),
    # บร.4 (id=10)
    (10, "photo/toilets/LC4-1_M.jpg"),
    (10, "photo/toilets/LC4-1_M2.jpg"),
    (10, "photo/toilets/LC4-1_W.jpg"),
    # บร.5 ฝั่งทางเดิน (id=11)
    (11, "photo/toilets/LC5-1_M.jpg"),
    (11, "photo/toilets/LC5-1_W.jpg"),
    # บร.5 ฝั่งศาลพระภูมิ (id=12)
    (12, "photo/toilets/LC5-2_M.jpg"),
    (12, "photo/toilets/LC5-2_W.jpg"),
    # บร.5 ฝั่งประตูทางเข้า (id=13)
    (13, "photo/toilets/LC5-3_M.jpg"),
    (13, "photo/toilets/LC5-3_W.jpg"),
    # บร.5 ฝั่งลานเก้าอี้ (id=14)
    (14, "photo/toilets/LC5-4_M.jpg"),
    (14, "photo/toilets/LC5-4_W.jpg"),
    # ศูนย์การเรียนรู้ (id=15)
    (15, "photo/toilets/SKR_M.jpg"),
    (15, "photo/toilets/SKR_W.jpg"),
    (15, "photo/toilets/SKR_D.jpg"),
    (15, "photo/toilets/SKR_D2.jpg"),
    # ป๋วยฯ ฝั่งใกล้ทางออก (id=16)
    (16, "photo/toilets/puey-1_M.jpg"),
    (16, "photo/toilets/puey-1_W.jpg"),
    (16, "photo/toilets/puey-1_D.jpg"),
    # ป๋วยฯ ฝั่งประตูเชื่อม (id=17)
    (17, "photo/toilets/puey-2_M.jpg"),
    (17, "photo/toilets/puey-2_W.jpg"),
    # ป๋วยฯ ฝั่ง co-learning (id=18)
    (18, "photo/toilets/puey-3_M.jpg"),
    (18, "photo/toilets/puey-3_W.jpg"),
]
        cursor.executemany("""
            INSERT INTO toilet_images (toilet_id, image_filename)
            VALUES (?, ?)
        """, IMAGES)

        conn.commit()
        print(f"Seeded ข้อมูลเรียบร้อยแล้ว")
    else:
        print("มีข้อมูลอยู่แล้ว ไม่ต้อง seed ใหม่")
    conn.close()