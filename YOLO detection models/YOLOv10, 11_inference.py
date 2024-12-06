# Inputs: root_dir = folder with images;
#         new_csv = detection csv to output
#         model_path = path to YOLOv8 weights file

root_dir = "C:/users/bpickens/Desktop/NPS Channel Islands"
new_csv = "C:/users/bpickens/Desktop/NPS_channel_islands_yolov10.csv"
model_path="C:/Users/bpickens/Desktop/MODELS FOR USE/seabird_yolov10_2024Q3.pt"

import torch
from sahi import AutoDetectionModel
import sahi.predict
import os
import csv
import pandas as pd

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
        result.export_visuals(file_name=base, export_dir="C:/Users/bpickens/Desktop/NPS Channel Islands/visuals_yolov10",
                hide_labels=True, hide_conf=False, rect_th=3)

        with open(new_csv, 'a', newline='') as file:
            writer = csv.writer(file)
            for result1 in object_prediction_list:
                writer.writerow([source, result1.bbox, result1.category, result1.score])
csv_data = pd.read_csv(new_csv)
csv_data['unique_image_jpg'] = csv_data['unique_image_jpg'].apply(os.path.basename)
bbox = csv_data['bbox']
csv_data['score'] = csv_data['score'].str.replace(r"PredictionScore: <value: ", '', regex=True)
csv_data['score'] = csv_data['score'].str.replace(r">", '', regex=True)
csv_data['class'] = csv_data['class'].str.replace(r"Category: <id:", '', regex=True)
csv_data['class'] = csv_data['class'].str.replace(r"name: ", '', regex=True)
csv_data['class'] = csv_data['class'].str.replace(r">", '', regex=True)
csv_data['bbox'] = csv_data['bbox'].str.replace(r"BoundingBox: <", '', regex= True)
csv_data['bbox'] = csv_data['bbox'].str.replace(r">", '', regex= True)
csv_data[['xmin', 'ymin', 'xmax', 'ymax', 'w', 'h']] = csv_data['bbox'].str.split(',', expand=True)
csv_data['h'] = csv_data['h'].str.replace(r"h: ", '', regex= True)
csv_data['w'] = csv_data['w'].str.replace(r"w: ", '', regex= True)
csv_data['xmin'] = csv_data['xmin'].str.replace(r"(", '', regex= False)

csv_data['temp_name'] = csv_data['unique_image_jpg'].str.replace(r".jpg", '', regex= True)

csv_data['xmin'] = csv_data['xmin'].astype(float).round().astype(int).astype(str)
csv_data['ymin'] = csv_data['ymin'].astype(float).round().astype(int).astype(str)
csv_data['w'] = csv_data['w'].astype(float).round().astype(int).astype(str)
csv_data['h'] = csv_data['h'].astype(float).round().astype(int).astype(str)

csv_data['ymin'].round(0)

#csv_data['w'].round(0)
#csv_data['h'].round(0)

csv_data['unique_BB'] = csv_data['temp_name'] + "_" + csv_data['xmin'] + "_" + csv_data['ymin'] + "_" + csv_data['w']+ "_" + csv_data['h']
del csv_data['bbox']
del csv_data['xmax']
del csv_data['ymax']
del csv_data['temp_name']

csv_data.to_csv(new_csv)

