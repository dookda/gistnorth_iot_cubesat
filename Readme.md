### setup environment
```bash
conda create --name fastapi python=3.8
conda activate fastapi
```

### install libraries
```bash
pip install fastapi uvicorn ultralytics opencv-python numpy
```

### run application
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### test application
```bash
curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{"image": "base64_encoded_image_string"}'
```

### test with RestClient
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

