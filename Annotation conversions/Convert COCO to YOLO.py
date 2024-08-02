{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "39c86353-32dd-4385-9a17-ddc66e3072fd",
   "metadata": {},
   "outputs": [],
   "source": [
    "# First, define the function needed\n",
    "import os\n",
    "import json\n",
    "from tqdm import tqdm\n",
    "import shutil\n",
    "\n",
    "def convert_bbox_coco2yolo(img_width, img_height, bbox):\n",
    "    \"\"\"\n",
    "    Convert bounding box from COCO  format to YOLO format\n",
    "    Parameters\n",
    "    ----------\n",
    "    img_width : int\n",
    "        width of image\n",
    "    img_height : int\n",
    "        height of image\n",
    "    bbox : list[int]\n",
    "        bounding box annotation in COCO format: \n",
    "        [top left x position, top left y position, width, height]\n",
    "\n",
    "    Returns\n",
    "    -------\n",
    "    list[float]\n",
    "        bounding box annotation in YOLO format: \n",
    "        [x_center_rel, y_center_rel, width_rel, height_rel]\n",
    "    \"\"\"  \n",
    "    # YOLO bounding box format: [x_center, y_center, width, height]\n",
    "    # (float values relative to width and height of image)\n",
    "    x_tl, y_tl, w, h = bbox\n",
    "\n",
    "    dw = 1.0 / img_width\n",
    "    dh = 1.0 / img_height\n",
    "\n",
    "    x_center = x_tl + w / 2.0\n",
    "    y_center = y_tl + h / 2.0\n",
    "\n",
    "    x = x_center * dw\n",
    "    y = y_center * dh\n",
    "    w = w * dw\n",
    "    h = h * dh\n",
    "\n",
    "    return [x, y, w, h]\n",
    "\n",
    "def make_folders(path=\"output\"):\n",
    "    if os.path.exists(path):\n",
    "        shutil.rmtree(path)\n",
    "    os.makedirs(path)\n",
    "    return path\n",
    "\n",
    "def convert_coco_json_to_yolo_txt(output_path, json_file):\n",
    "    path = make_folders(output_path)\n",
    "    with open(json_file) as f:\n",
    "        json_data = json.load(f)\n",
    "\n",
    "    # write _darknet.labels, which holds names of all classes (one class per line)\n",
    "    label_file = os.path.join(output_path, \"_darknet.labels\")\n",
    "    with open(label_file, \"w\") as f:\n",
    "        for category in tqdm(json_data[\"categories\"], desc=\"Categories\"):\n",
    "            category_name = category[\"name\"]\n",
    "            f.write(f\"{category_name}\\n\")\n",
    "\n",
    "    for image in tqdm(json_data[\"images\"], desc=\"Annotation txt for each iamge\"):\n",
    "        img_id = image[\"id\"]\n",
    "        img_name = image[\"file_name\"]\n",
    "        img_width = image[\"width\"]\n",
    "        img_height = image[\"height\"]\n",
    "\n",
    "        anno_in_image = [anno for anno in json_data[\"annotations\"] if anno[\"image_id\"] == img_id]\n",
    "        anno_txt = os.path.join(output_path, img_name.split(\".\")[0] + \".txt\")\n",
    "        with open(anno_txt, \"w\") as f:\n",
    "            for anno in anno_in_image:\n",
    "                category = anno[\"category_id\"]\n",
    "                bbox_COCO = anno[\"bbox\"]\n",
    "                x, y, w, h = convert_bbox_coco2yolo(img_width, img_height, bbox_COCO)\n",
    "                f.write(f\"{category} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\\n\")\n",
    "\n",
    "    print(\"Converting COCO Json to YOLO txt finished!\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "2d638e57-fd40-4095-9da1-5fd5ec37904b",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "Categories: 100%|████████████████████████████████████████████████████████████████████████████████| 3/3 [00:00<?, ?it/s]\n",
      "Annotation txt for each iamge: 100%|████████████████████████████████████████████| 87547/87547 [02:46<00:00, 526.05it/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Converting COCO Json to YOLO txt finished!\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\n"
     ]
    }
   ],
   "source": [
    "# Inputs: (directory for yolo outputs, coco json input file) \n",
    "convert_coco_json_to_yolo_txt(\"C:/Users/bpickens/Desktop/SACR_detection/temp1/train/labels\", \n",
    "                              \"C:/Users/bpickens/Desktop/SACR_detection/hive batch2 COCO.json\")"
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
