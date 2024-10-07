## The foundation for this code was from: https://github.com/KapilM26/coco2VOC
# We are extremely grateful from this contribution! Thank you!

from pycocotools.coco import COCO
from pascal_voc_writer import Writer
import argparse
import os

# Inputs
## ann_file = COCO annotation json
## output_dir = directory for output PASCAL Voc annotations
ann_file = "D:/hive_detection/hive_all_annot_Oct2024_COCO.json"
output_dir = "D:/hive_detection/hive_annot_voc/"

def coco2voc(ann_file, output_dir):
    coco = COCO(ann_file)
    # cats = class categories
    cats = coco.loadCats(coco.getCatIds())
    cat_idx = {}
    for c in cats:
        cat_idx[c['id']] = c['name']
    for img in coco.imgs:
        catIds = coco.getCatIds()
        annIds = coco.getAnnIds(imgIds=[img], catIds=catIds)
        if len(annIds) > 0:
            img_fname = coco.imgs[img]['file_name']
            print("img_fname:" , img_fname)
            image_fname_ls = img_fname.split('.')
            image_fname_ls[-1] = 'xml'
            label_fname = '.'.join(image_fname_ls)
            print("label_fname", label_fname)
            writer = Writer(img_fname, coco.imgs[img]['width'], coco.imgs[img]['height'])
            anns = coco.loadAnns(annIds)
            for a in anns:
                bbox = a['bbox']
                bbox = [bbox[0], bbox[1], bbox[2] + bbox[0], bbox[3] + bbox[1]]
                bbox = [str(b) for b in bbox]
               # print(bbox)
                catname = cat_idx[a['category_id']]
                writer.addObject(catname, bbox[0], bbox[1], bbox[2], bbox[3])

                basename = os.path.basename(label_fname)
                print("basename:", basename)
                writer.save(output_dir+'/'+ basename)

coco2voc(ann_file=ann_file, output_dir= output_dir)