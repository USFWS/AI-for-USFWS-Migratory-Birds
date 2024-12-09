from sahi import AutoDetectionModel
import sahi.predict
import os
import csv
import torch
from ultralytics import YOLO

# YOLOv5 training is done on the command line!
# For inference that outputs a csv file with detections:
# Inputs: root_dir = folder with images;
#         new_csv = detection csv to output
#         model_path = path to YOLOv8 weights file

root_dir = "D:/AMAPPS/2024-0826_800AGL/JPG_2024_aug26"
new_csv = "D:/AMAPPS/YOLOv8_2024_Aug26xx.csv"
model_path="D:/models/yolo_2023.3_Q4.pt"

device = "cuda:1" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")
use_cuda = torch.cuda.is_available()
if device:
    print(torch.cuda.get_device_name())

detection_model = AutoDetectionModel.from_pretrained(
    model_type='yolov5',
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
        #   hide_conf=True, rect_th=2)

        with open(new_csv, 'a', newline='') as file:
            writer = csv.writer(file)
            for result1 in object_prediction_list:
                writer.writerow([source, result1.bbox, result1.category, result1.score])

csv_data = pd.read_csv(new_csv)

filename = csv_data['unique_image_jpg']
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
del csv_data['bbox']

csv_data.to_csv(new_csv)