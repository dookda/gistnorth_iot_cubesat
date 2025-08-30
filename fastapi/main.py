from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse, Response
from ultralytics import YOLO
import numpy as np
import cv2
import time

app = FastAPI()
model = YOLO("yolo11n.pt")  # เปลี่ยนเป็นโมเดลที่ต้องการใช้

# create api to receive image and save to image folder


@app.post("/upload")
async def upload_image(request: Request):
    image_bytes = await request.body()
    # add to image folder and ass suffix with timestamp
    timestamp = int(time.time())
    with open(f"image/image_{timestamp}.jpg", "wb") as f:
        f.write(image_bytes)
    return {"message": "Image uploaded successfully"}


@app.get("/")
def read_root():
    return {"message": "Welcome to the YOLO object detection API"}


def run_infer(image_bytes: bytes):
    arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)  # img เป็น BGR (เหมาะกับ OpenCV)
    results = model.predict(source=img, imgsz=640, conf=0.25, verbose=False)
    return img, results[0]


@app.post("/infer")
async def infer(
    request: Request,
    render: bool = Query(
        False, description="true = ส่งคืนรูปภาพ JPEG ที่ตีกรอบ")
):
    image_bytes = await request.body()
    _, r = run_infer(image_bytes)

    # ตรวจสอบ Accept header แบบไม่ติดเคส
    accept = (request.headers.get("accept") or "").lower()
    wants_image = "image/" in accept

    if render or wants_image:
        annotated = r.plot(line_width=2, labels=True,
                           conf=True)  # ndarray (BGR)
        ok, buf = cv2.imencode(".jpg", annotated)
        if not ok:
            return Response(status_code=500, content="Failed to encode image")
        return Response(
            content=buf.tobytes(),
            media_type="image/jpeg",
            # ช่วยให้ client แสดง inline
            headers={"Content-Disposition": "inline; filename=annotated.jpg"}
        )

    # คืน JSON ตามเดิม
    dets = []
    names = r.names
    for b in r.boxes:
        x1, y1, x2, y2 = map(float, b.xyxy[0].tolist())
        cls_id = int(b.cls[0])
        conf = float(b.conf[0])
        dets.append({"bbox": [x1, y1, x2, y2], "cls_id": cls_id,
                     "cls_name": names[cls_id], "conf": conf})
    return JSONResponse({"detections": dets, "image_shape": r.orig_shape})
