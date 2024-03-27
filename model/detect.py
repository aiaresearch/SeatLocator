import os
from ultralytics import YOLO

def list_files(directory):
    file_names = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_names.append(os.path.join(root, file))
    return file_names

folder_path = 'test'
model = YOLO('weights/best.pt')
files = list_files(folder_path)

for file in files:
    predictions = model.predict(file, save=True, imgsz=640, conf=0.5, iou=0.5)
    