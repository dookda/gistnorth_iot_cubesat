## คู่มืออบรม: ระบบเก็บภาพจาก ESP32‑CAM ด้วย FastAPI, YOLO และหน้าเว็บ
### 1. เตรียมสภาพแวดล้อมด้วย Conda
การใช้ Conda ช่วยให้จัดการแพ็กเกจและสภาพแวดล้อมของ Python ได้สะดวก โดยเฉพาะเมื่อต้องใช้ไลบรารีที่มีการอ้างอิงซับซ้อน เช่น FastAPI และ YOLO (Ultralytics)

### 1.1 ติดตั้ง Conda
ดาวน์โหลด Miniconda หรือ Anaconda ตามระบบปฏิบัติการจากหน้าเว็บทางการ

ติดตั้งตามขั้นตอนที่ตัวติดตั้งแนะนำ

<!-- list -->
- หากใช้ Linux/Mac สามารถใช้ไฟล์ .sh
- หากใช้ Windows ใช้ไฟล์ .exe

เมื่อติดตั้งเสร็จ เปิดเทอร์มินัล/Command Prompt ใหม่ เพื่อให้คำสั่ง conda พร้อมใช้งาน

### 1.2 สร้างและใช้งานสภาพแวดล้อม
สร้าง environment ชื่อ esp32cam พร้อม Python 3.10

```bash
conda create -n fastapi python=3.10
```
เปิดใช้งาน environment

```bash
conda activate fastapi
```
เมื่อเปิดใช้งานสำเร็จ ชื่อ environment จะปรากฏหน้าพรอมต์ (เช่น (fastapi))

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


## 2. สร้าง FastAPI สำหรับเก็บข้อมูล image
- สร้างโครงสร้างโฟลเดอร์: main.py, images/, static/
```csharp
fastapi/
├── main.py          # แอปหลัก
├── images/          # โฟลเดอร์เก็บภาพที่อัปโหลด
├── static/          # หน้าเว็บ front-end
└── yolo11n.pt       # โมเดล YOLO ใช้วิเคราะห์รูป
```
- ดาวน์โหลดโมเดล YOLO จาก [ที่นี่](https://github.com/AlexeyAB/darknet/releases)

สร้างไฟล์ main.py ด้วยโค้ดดังนี้:
```python
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os

app = FastAPI()

app.mount("/web", StaticFiles(directory="static"), name="static")

@app.get("/api")
def read_root():
    return {"Hello": "World"}
```

- เพิ่มฟังก์ชันเพื่ออัปโหลดและเก็บภาพ

สร้าง API:

- POST /upload รับและบันทึกรูป

```python
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        with open(f"images/{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"filename": file.filename}
    except Exception as e:
        return {"error": str(e)}
- GET /images คืนรายการไฟล์

```python
@app.get("/images")
def list_images():
    images = os.listdir("images")
    return {"images": images}
```

- GET /infer/{image}?render=true|false วิเคราะห์วัตถุด้วย YOLO

```python
@app.get("/infer/{image}")
def infer_image(image: str, render: bool = False):
    # รัน YOLO บนภาพที่ระบุ
    return {"image": image, "render": render}
```

- รันเซิร์ฟเวอร์ด้วย uvicorn main:app --reload --host 0.0.0.0 --port 8000

## 3. การใช้งาน ESP32‑CAM
### 3.1 เชื่อมต่อฮาร์ดแวร์
อุปกรณ์หลัก:
- โมดูล ESP32‑CAM
- USB‑to‑TTL (FTDI/CP2102/CH340)
- สาย jumper 6 เส้น

การต่อสายพื้นฐาน:
<!-- table -->
| ESP32-CAM Pin | USB‑TTL Pin |
|----------------|-------------|
| U0R            | TX          |
| U0T            | RX          |
| GND            | GND         |
| 5V             | 5V          |

- เข้าสู่โหมดแฟลช: กดปุ่ม GPIO0 หรือจัมเปอร์ IO0→GND แล้วกด RST (หรือจ่ายไฟใหม่)

### 3.2 ตั้งค่า Arduino IDE
- ติดตั้ง Arduino IDE ดาวน์โหลดจาก [เว็บไซต์ Arduino](https://www.arduino.cc/en/software)
- เปิด Arduino IDE และไปที่ Preferences
- เพิ่ม URL ของบอร์ด ESP32 ใน Additional Board Manager URLs
   https://dl.espressif.com/dl/package_esp32_index.json
- เพิ่มบอร์ด ESP32 จาก Board Manager
  - ค้นหา "esp32"
  - ติดตั้งบอร์ด ESP32 by Espressif Systems

- เลือกบอร์ด ESP32‑CAM จาก Tools > Board > ESP32 Arduino > AI Thinker ESP32-CAM
- ตั้งค่าพอร์ต (Tools > Port) ให้ตรงกับพอร์ตที่เชื่อมต่อ USB‑TTL

### 3.3 ทดลองเขียนโค้ด
- เขียนโค้ด print hello ทุกๆ 30 วินาที
```cpp
#include "esp_camera.h"
#include <WiFi.h>
#include <HTTPClient.h>

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("Hello");
}

void loop() {
  delay(30000);
  Serial.println("Hello");
}
```
- อัปโหลดโค้ดไปยังบอร์ดและทดสอบผ่าน Serial Monitor

### 3.4 เขียนโค้ดถ่ายภาพ
- เขียนโค้ดถ่ายภาพแล้วส่งผ่าน HTTP POST ไปยังเซิร์ฟเวอร์ (/upload)

```cpp
#include "esp_camera.h"
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverUrl = "http://<server-ip>:8000/upload"; // FastAPI endpoint

// กำหนดพินตามโมดูล AI-Thinker
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

void startCameraServer() {}

void setup() {
  Serial.begin(115200);
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size = FRAMESIZE_SVGA;
  config.jpeg_quality = 12;
  config.fb_count = 1;

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed: %s\n", esp_err_to_name(err));
    return;
  }

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");
}

void sendImage() {
  camera_fb_t* fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  }

  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "image/jpeg");

  int httpResponseCode = http.POST(fb->buf, fb->len);
  if (httpResponseCode > 0) {
    Serial.printf("Image sent, response: %d\n", httpResponseCode);
  } else {
    Serial.printf("Failed sending image, error: %s\n", http.errorToString(httpResponseCode).c_str());
  }

  http.end();
  esp_camera_fb_return(fb);
}

void loop() {
  sendImage();
  delay(10000); // ส่งทุก 10 วินาที
}
```
- อัปโหลดโค้ดไปยังบอร์ดและทดสอบผ่าน Serial Monitor


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