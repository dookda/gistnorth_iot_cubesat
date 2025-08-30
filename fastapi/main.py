from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO
import numpy as np
import cv2
import time
import os

app = FastAPI()
model = YOLO("yolo11n.pt")  # เปลี่ยนเป็นโมเดลที่ต้องการใช้

app.mount("/web", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")


@app.get("/")
def read_root():
    timestamp = int(time.time())
    return {"message": "Welcome to the YOLO object detection API at " + str(timestamp)}


@app.post("/upload")
async def upload_image(request: Request):
    image_bytes = await request.body()
    timestamp = int(time.time())
    file_path = f"images/image_{timestamp}.jpg"
    with open(file_path, "wb") as f:
        f.write(image_bytes)
    return {"message": "Image uploaded successfully at " + str(timestamp)}


@app.get("/images")
def list_images():
    print("dd")
    image_files = os.listdir("images")
    return {"images": image_files}


def run_infer_from_file(image_path: str):
    """Load image from file and run inference"""
    if not os.path.exists(image_path):
        raise HTTPException(
            status_code=404, detail=f"Image file not found: {image_path}")

    img = cv2.imread(image_path)
    if img is None:
        raise HTTPException(
            status_code=400, detail=f"Could not read image file: {image_path}")

    results = model.predict(source=img, imgsz=640, conf=0.25, verbose=False)
    return img, results[0]


@app.get("/infer/{image_name}")
async def infer_by_name(
    image_name: str,
    render: bool = Query(
        False, description="true = ส่งคืนรูปภาพ JPEG ที่ตีกรอบ")
):
    image_path = os.path.join("images", image_name)
    _, r = run_infer_from_file(image_path)

    if render:
        annotated = r.plot(line_width=2, labels=True, conf=True)
        ok, buf = cv2.imencode(".jpg", annotated)
        if not ok:
            return Response(status_code=500, content="Failed to encode image")
        return Response(
            content=buf.tobytes(),
            media_type="image/jpeg",
            headers={"Content-Disposition": "inline; filename=annotated.jpg"}
        )

    # คืน JSON
    dets = []
    names = r.names
    for b in r.boxes:
        x1, y1, x2, y2 = map(float, b.xyxy[0].tolist())
        cls_id = int(b.cls[0])
        conf = float(b.conf[0])
        dets.append({"bbox": [x1, y1, x2, y2], "cls_id": cls_id,
                     "cls_name": names[cls_id], "conf": conf})
    return JSONResponse({"detections": dets, "image_shape": r.orig_shape})
