# Inputs: root_dir = folder with images;
#         new_csv = detection csv to output
#         model_path = path to YOLOv8 weights file

root_dir = "D:/AMAPPS/2024-0826_800AGL/JPG_2024_aug26"
new_csv = "D:/AMAPPS/YOLOv8_2024_Aug26.csv"
model_path="D:/models/yolo_2023.3_Q4.pt"

import torch
from sahi import AutoDetectionModel
import sahi.predict
import os
import csv

device = "cuda:1" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

detection_model = AutoDetectionModel.from_pretrained(
    model_type='yolov8',
    model_path=model_path,
    confidence_threshold=0.7,
    device="cuda:1",  # or 'cuda:0'
)

with open(new_csv, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['unique_image_jpg', "bbox", "class", "score"])

for root, dirs, files in os.walk(root_dir):
    for file in files:
        source = os.path.join(root, file)
        print(source)
        result = sahi.predict.get_sliced_prediction(
            source,
            detection_model,
            slice_height=1024,
            slice_width=1024,
            overlap_height_ratio=0.0,
            overlap_width_ratio=0.0)
        object_prediction_list = result.object_prediction_list
        base = os.path.basename(file)
        # result.export_visuals(file_name=base, export_dir="C:/Users/Aware/Desktop/visuals", hide_labels=True,
                  #            hide_conf=True, rect_th=2)

        with open(new_csv, 'a', newline='') as file:
            writer = csv.writer(file)
            for result1 in object_prediction_list:
                writer.writerow([source, result1.bbox, result1.category, result1.score])
