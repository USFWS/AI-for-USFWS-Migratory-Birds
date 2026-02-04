# Use label-studio interpreter

import label_studio_sdk.converter.imports.coco
import pandas as pd
import json
from label_studio_sdk import converter

## Inputs: csv_file = csv with annotation data; Please see csv_data.columns below and the Label-studio
# csv template in the github folder for specifications
# categories = input label index corresponding to names of your labels
# output_file = name of label studio json to export
# config = name of label studio config file to export; can be used as labeling interface
# image_width, image_height

csv_file = "D:/SACR/SACR_FIX/2025_annot_preds_June23.csv"
categories = [{"id":0, "name": "sandhill_crane"}]

output_file = "D:/SACR/SACR_FIX/2025_annot_preds_June23_LS.json"
#config = "C:/Users/name/Desktop/SACR_detection/YOLO8_SACR_mixed_train_March14_LS_config_temp.xml"
image_width = 736
image_height = 736

csv_data = pd.read_csv(csv_file)
csv_data['image_id']= csv_data['image_id'].astype(int) # change data types, as needed
# csv_data.columns = (['image_id','xmin', 'ymin', 'w','h','label_id','label', 'root_url','unique_image_jpg',
                 #   'score'])
csv_data['annid'] = csv_data.index

# Create lists to fill in, including nested dictionaries
#categories = []
images = []
annotations = []

def image(row):
    image = {}
    # height and width of parent image
    image["width"] = image_width
    image["height"] = image_height
    image["id"] = row.image_id
    image["file_name"] = row.unique_image_jpg
    image["root_url"] = row.root_url

  #  image["observer"] = row.author
    return image

def annotation(row):
    annotation = {}
    #annotation["id"] = row.annid
    annotation["image_id"] = row.image_id
    annotation["category_id"] = row.label_id
    annotation["bbox"] = [row.xmin, row.ymin, row.w, row.h]
    annotation["ignore"] = 0
    annotation["iscrowd"] = 0
    annotation["area"] = (row.h * row.w)
    annotation["score"] = row.score
    return annotation

# Iterates through rows
for index, row in csv_data.iterrows():
    annotations.append(annotation(row))
    images.append(image(row))
len(images)

# remove duplicate images
images2 = []

imagedf = csv_data.drop_duplicates(subset=['image_id'])
for index, row in imagedf.iterrows():
    images2.append(image(row))

# Remove duplicate images
data_coco = {}
data_coco["images"] = images2
data_coco["categories"] = categories
data_coco["annotations"] = annotations
#json dump uses a dict as input

coco_output = open('D:/SACR/SACR_FIX/June23_preds.json', 'w')
json.dump(data_coco, coco_output)
coco_output.close()

label_studio_sdk.converter.imports.coco.convert_coco_to_ls('D:/SACR/SACR_FIX/June23_preds.json', "D:/SACR/SACR_FIX/2025_pred_LS.json", out_type= "predictions", image_root_url= ' /data/images/')
# use 'predictions' or 'results', depending on your application