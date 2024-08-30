{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "dc21ef73",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "okay\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "91"
      ]
     },
     "execution_count": 2,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import os\n",
    "import pandas as pd\n",
    "import json\n",
    "import csv\n",
    "import numpy as np\n",
    "from label_studio_converter import coco\n",
    "\n",
    "os.chdir(\"C:/Users/dir\")\n",
    "os.getcwd()\n",
    "\n",
    "## Inputs: csv_file = csv with annotation data; Please see csv_data.columns below and the Label-studio \n",
    "# csv template in the github folder for specifications\n",
    "# categories = input label index corresponding to names of your labels\n",
    "# Inputs- output_file = name of label studio json to export\n",
    "#  config = name of label studio config file to export; can be used as labeling interface\n",
    "\n",
    "csv_file = 'YOLO8_SACR_mixed_train_March14.csv'\n",
    "categories = [{\"id\":0, \"name\": \"duck_goose\"},{\"id\":1, \"name\": \"sandhill crane\"}]\n",
    "#categories.append(category)\n",
    "\n",
    "output_file = \"C:/Users/dirbpickens/Desktop/SACR_detection/YOLO8_SACR_mixed_train_March14_LS.json\"\n",
    "config = \"C:/Users/bpickens/Desktop/SACR_detection/YOLO8_SACR_mixed_train_March14_LS_config_temp.xml\"\n",
    "\n",
    "dtype = {'image_id': str, 'label_id': np.int64}\n",
    "\n",
    "csv_data = pd.read_csv(csv_file, dtype=dtype) \n",
    "csv_data['image_id']= csv_data['image_id'].astype(int)\n",
    "csv_data.columns = (['id','image_id','x_min', 'y_min', 'w','h','label_id','label', 'root_url','unique_image_jpg', \n",
    "                    'score'])\n",
    "csv_data['annid'] = csv_data.index\n",
    "\n",
    "print(\"okay\")\n",
    "\n",
    "# Create 3 major lists to fill in, including nested dictionaries\n",
    "#categories = []\n",
    "images = []\n",
    "annotations = []\n",
    "\n",
    "def image(row):\n",
    "    image = {}\n",
    "    # height and width of parent image\n",
    "    image[\"width\"] = 736\n",
    "    image[\"height\"] = 736\n",
    "    image[\"id\"] = row.image_id\n",
    "    image[\"file_name\"] = row.unique_image_jpg\n",
    "    image[\"root_url\"] = row.root_url\n",
    "  #  image[\"observer\"] = row.author\n",
    "    return image\n",
    "\n",
    "def annotation(row):\n",
    "    annotation = {}\n",
    "    #annotation[\"id\"] = row.annid\n",
    "    annotation[\"image_id\"] = row.image_id\n",
    "    annotation[\"category_id\"] = row.label_id\n",
    "    annotation[\"bbox\"] = [row.x_min, row.y_min, row.w, row.h]\n",
    "    annotation[\"ignore\"] = 0\n",
    "    annotation[\"iscrowd\"] = 0\n",
    "    annotation[\"area\"] = (row.h * row.w)\n",
    "    annotation[\"score\"] = row.score\n",
    "    return annotation\n",
    "\n",
    "# Iterates through rows\n",
    "for index, row in csv_data.iterrows():\n",
    "    annotations.append(annotation(row))\n",
    "    images.append(image(row))   \n",
    "len(images)\n",
    "\n",
    "# remove duplicate images\n",
    "images2 = []\n",
    "\n",
    "imagedf = csv_data.drop_duplicates(subset=['image_id'])\n",
    "for index, row in imagedf.iterrows():\n",
    "    images2.append(image(row)) \n",
    "\n",
    "# Remove duplicate images\n",
    "data_coco = {}\n",
    "data_coco[\"images\"] = images2\n",
    "data_coco[\"categories\"] = categories\n",
    "data_coco[\"annotations\"] = annotations\n",
    "#json dump uses a dict as input\n",
    "json.dump(data_coco, open(export_json,\"w\"), indent=0)\n",
    "\n",
    "input_file = export_json\n",
    "\n",
    "coco.convert_coco_to_ls(input_file,output_file, out_type='predictions')\n",
    "# use 'predictions' or 'results', depending on your application"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
