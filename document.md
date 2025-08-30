##คู่มืออบรม: ระบบเก็บภาพจาก ESP32‑CAM ด้วย FastAPI, YOLO และหน้าเว็บ
### 1. เตรียมสภาพแวดล้อมด้วย Conda
การใช้ Conda ช่วยให้จัดการแพ็กเกจและสภาพแวดล้อมของ Python ได้สะดวก โดยเฉพาะเมื่อต้องใช้ไลบรารีที่มีการอ้างอิงซับซ้อน เช่น FastAPI และ YOLO (Ultralytics)

### 1.1 ติดตั้ง Conda
ดาวน์โหลด Miniconda หรือ Anaconda ตามระบบปฏิบัติการจากหน้าเว็บทางการ

ติดตั้งตามขั้นตอนที่ตัวติดตั้งแนะนำ

<!-- list -->
- ผู้ใช้ Linux/Mac สามารถใช้ไฟล์ .sh
- ผู้ใช้ Windows ใช้ไฟล์ .exe

เมื่อติดตั้งเสร็จ เปิดเทอร์มินัล/Command Prompt ใหม่ เพื่อให้คำสั่ง conda พร้อมใช้งาน

### 1.2 สร้างและใช้งานสภาพแวดล้อม
สร้าง environment ชื่อ esp32cam พร้อม Python 3.10

```bash
conda create -n esp32cam python=3.10
```
เปิดใช้งาน environment

```bash
conda activate esp32cam
```
เมื่อเปิดใช้งานสำเร็จ ชื่อ environment จะปรากฏหน้าพรอมต์ (เช่น (esp32cam))

### 1.3 ติดตั้งไลบรารีหลัก
FastAPI และ Uvicorn (ใช้ช่อง conda-forge เพื่อเวอร์ชันล่าสุด)

```bash
conda install fastapi uvicorn -c conda-forge
```
OpenCV (จำเป็นสำหรับการบันทึกและแสดงผลภาพ)

```bash
conda install opencv -c conda-forge
```
YOLO (Ultralytics) – ไม่มีแพ็กเกจ conda อย่างเป็นทางการ จึงติดตั้งผ่าน pip ภายใน environment

```bash
pip install ultralytics
```
ตรวจสอบว่าไลบรารีทั้งหมดติดตั้งครบ

```bash
python -c "import fastapi, cv2, ultralytics; print('OK')"
```

### 1.4 จัดการ environment ด้วยไฟล์ environment.yml (ทางเลือก)
สร้างไฟล์บันทึกรายการแพ็กเกจ

conda env export > environment.yml
สร้าง environment จากไฟล์
```bash
conda env create -f environment.yml
```
ขั้นตอนนี้ช่วยให้ผู้เรียนทุกคนมีสภาพแวดล้อมเหมือนกัน ลดปัญหาความแตกต่างของเวอร์ชันและแพ็กเกจ

## 2. การใช้งาน ESP32‑CAM
เชื่อมต่อฮาร์ดแวร์ (ESP32‑CAM, USB‑to‑TTL, สายไฟ 5 V ฯลฯ)

ตั้งค่า Arduino IDE, เพิ่มบอร์ด ESP32 และไลบรารี esp_camera, WiFi, HTTPClient

เขียนโค้ดถ่ายภาพแล้วส่งผ่าน HTTP POST ไปยังเซิร์ฟเวอร์ (/upload)

อัปโหลดโค้ดไปยังบอร์ดและทดสอบผ่าน Serial Monitor

## 3. สร้าง FastAPI สำหรับเก็บข้อมูล image
โครงสร้างโฟลเดอร์: main.py, images/, static/, โมเดล yolo11n.pt

ภายใน environment ที่สร้างด้วย Conda ติดตั้งไลบรารีเพิ่มเติม (หากยังไม่ได้ติดตั้ง)

สร้าง API:

- POST /upload รับและบันทึกรูป

- GET /images คืนรายการไฟล์

- GET /infer/{image}?render=true|false วิเคราะห์วัตถุด้วย YOLO

รันเซิร์ฟเวอร์ด้วย uvicorn main:app --reload --host 0.0.0.0 --port 8000

## 4. สร้าง front‑end สำหรับเรียกดูภาพ
สร้างหน้า static/index.html ใช้ Bootstrap จัดเลย์เอาต์

เขียนสคริปต์ JavaScript:

loadImages() ดึงรายชื่อไฟล์จาก GET /images

showImage(name) โหลดภาพผลลัพธ์จาก /infer/{name}?render=true

เปิดเบราว์เซอร์ที่ http://<ip>:8000/web/ เพื่อทดสอบการแสดงผล

สรุป
Conda environment ช่วยให้ติดตั้งและจัดการ FastAPI + YOLO อย่างเป็นระบบ

ESP32‑CAM ส่งภาพแบบ POST ไปยัง API

FastAPI รับภาพ เก็บไว้ และวิเคราะห์ด้วย YOLO

Front‑End โหลดรูปจาก API และแสดงผลแบบโต้ตอบ

ระบบที่ได้สามารถใช้เป็นฐานสำหรับการพัฒนาแอปพลิเคชัน IoT หรือระบบวิเคราะห์ภาพเพิ่มเติมในอนาคตได้อย่างยืดหยุ่น.