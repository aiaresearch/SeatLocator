import time
import cv2
from collections import defaultdict
from ultralytics import YOLO
import requests
import os
password = os.getenv("PASSWORD")
model = YOLO('/home/pi/Desktop/best.pt')
cap = cv2.VideoCapture(0)
with open('请在该文档中更改设备序列.txt', 'r') as file:
    lines = file.readlines()
    id = lines[0].strip()
    url = f"http://47.120.18.45:80/update_data_{id}"

while True:
    if not cap.isOpened(): 
        print('无法打开摄像头')
        break
    ret, frame = cap.read()
    if ret:
        results = model.predict(frame, conf=0.5, save=False, imgsz=640, iou=0.5)
        class_names = model.names
        class_counts = defaultdict(int)

        for result in results:
            boxes = result.boxes
            for i in range(len(boxes)):
                class_index = int(boxes.cls[i])
                class_name = class_names[class_index]
                class_counts[class_name] += 1
            if class_counts=={}:
                print("No objects detected")
                class_counts={"occupied":0, "available":0}
            elif len(class_counts)==1:
                if "occupied" in class_counts:
                    class_counts["available"]=0
                elif "available" in class_counts:
                    class_counts["occupied"]=0
        
        print(class_counts)
        class_counts['password'] = password
        
        response = requests.post(url, json=class_counts)

        if response.status_code == 200:
            print("请求成功")
        elif response.status_code == 404:
            print("请求的资源未找到")
        elif response.status_code == 500:
            print("服务器内部错误")
        else:
            print("请求失败，状态码：", response.status_code)
    
    time.sleep(20)
cap.release()