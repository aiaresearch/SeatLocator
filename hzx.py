import json
from collections import defaultdict
from ultralytics import YOLO

# 加载YOLOv模型
model = YOLO('D:/Library_seat_query/detection/train4/train4/weights/best.pt')

results = model.predict("test6.jpg", conf=0.5,iou=0.5)

# 获取类别名称列表
class_names = model.names

# 创建一个空字典来存储每个类别的数量
class_counts = defaultdict(int)

for result in results:
    # 获取检测框对象
    boxes = result.boxes
    
    # 循环遍历每个检测框
    for i in range(len(boxes)):
        # 获取当前检测框的类别索引
        class_index = int(boxes.cls[i])
        
        # 使用类别索引获取类别名称
        class_name = class_names[class_index]
        
        # 增加对应类别的计数
        class_counts[class_name] += 1

# 将字典转换为JSON格式字符串
json_string = json.dumps(class_counts)

# 打印JSON格式字符串
print(json_string)
