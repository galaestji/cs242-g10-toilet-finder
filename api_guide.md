# 🚻 Campus Toilet Finder API

Backend API สำหรับค้นหาห้องน้ำที่ใกล้ที่สุด โดยใช้พิกัด GPS ของผู้ใช้

---

## 🔧 Tech Stack
- Python (Flask)
- REST API
- JSON
- Haversine Algorithm

---

## 🚀 How to Run

1. ติดตั้ง dependencies

```bash
pip install flask
```

2. รัน server

```bash
python app.py
```

3. เปิดใช้งาน

```
http://127.0.0.1:5000
```

---

## 📡 API Endpoint

### POST /api/nearest

ใช้สำหรับค้นหาห้องน้ำที่ใกล้ที่สุด

---

## 📥 Request Body (JSON)

```json
{
  "lat": number,
  "lon": number
}
```

### Example

```json
{
  "lat": 18.8040,
  "lon": 98.9503
}
```

---

## 📤 Response

```json
[
  {
    "name": "Toilet Name",
    "floor": "1",
    "info": "รายละเอียด",
    "lat": 18.80,
    "lon": 98.95,
    "map_link": "https://www.google.com/maps?q=..."
  }
]
```

---

## 💻 Example Usage (Frontend)

```javascript
fetch("http://127.0.0.1:5000/api/nearest", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    lat: userLat,
    lon: userLon
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

---

## ⚠️ Notes
- Backend รันที่ port 5000
- ต้องเปิด Flask server ก่อนใช้งาน
- หาก frontend อยู่คนละ port อาจต้องเปิด CORS

---

## 🧠 System Overview
1. รับพิกัดผู้ใช้ (GPS)
2. คำนวณระยะทางด้วย Haversine Algorithm
3. เลือกห้องน้ำที่ใกล้ที่สุด 3 อันดับ
4. ส่งผลลัพธ์กลับเป็น JSON พร้อม Google Maps link

---

## 🗄️ Database Backup

ระบบมี automation script สำหรับสำรองฐานข้อมูล `toilets.db` โดยอัตโนมัติ

### วิธีใช้

```bash
python backup.py
```

### การทำงาน
- สำรองไฟล์ `toilets.db` ไปยังโฟลเดอร์ `backups/`
- ตั้งชื่อไฟล์ตาม timestamp เช่น `toilets_backup_20260501_140050.db`
- เก็บ backup ล่าสุดไว้ 5 ชุด และลบอันเก่าออกอัตโนมัติ

### ตัวอย่าง Output

```
Backup saved: backups\toilets_backup_20260501_140050.db (16.0 KB)
```
