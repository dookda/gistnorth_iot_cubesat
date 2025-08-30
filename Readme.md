### 1.setup fastapi 
#### 1.1 setup conda environment
```bash
conda create --name fastapi python=3.8
conda activate fastapi
```

#### 1.2 install libraries
```bash
pip install fastapi uvicorn ultralytics opencv-python numpy
```

#### 1.3 run application
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### 1.4 test with curl
```bash
curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{"image": "base64_encoded_image_string"}'
```

#### 1.5 test with RestClient
```bash
### upload image
POST http://localhost:8000/upload
Content-Type: application/octet-stream
Accept: application/json

< ./test2.jpg

### ขอผลเป็นรูป JPEG (ตีกรอบแล้ว)
POST http://localhost:8000/infer?render=true
Content-Type: application/octet-stream
Accept: image/jpeg

< ./test2.jpg


### ขอผลเป็น JSON (ไม่ตีกรอบ)
POST http://localhost:8000/infer
Content-Type: application/octet-stream
Accept: application/json

< ./test2.jpg    
```

### 2.setup ngRok
#### 2.1 download and install ngrok
```bash
https://ngrok.com/download
```

#### create tunnel
```bash
ngrok http 8000
```

### 3. setup Platformio
#### 3.1 install Platformio extension in VSCode
```bash
code --install-extension platformio.platformio-ide
```

#### 3.2 config Platformio.ini
```bash
[env:esp32cam]
platform = espressif32
board = esp32cam
framework = arduino

monitor_speed = 115200
upload_port = /dev/tty.usbserial-XXXX
monitor_port = /dev/tty.usbserial-XXXX
```
