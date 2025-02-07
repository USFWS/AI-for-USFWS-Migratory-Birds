import os
import torch
import image_bbox_tiler as ibis

# Inputs: im_src = image source directory, an_src = annotation source directory
im_src = "C:/Brad/a_detection_of_seabirds/hive_images_not_reviewed"
an_src = "C:/Brad/a_detection_of_seabirds/hive_annot_not_reviewed/"

# Inputs: im_dst = destination of tiles, an_dst = destination of annotations
im_dst = "C:/Brad/a_detection_of_seabirds/tiles_not_reviewed_w_empties/"
an_dst = "C:/Brad/a_detection_of_seabirds/tile_annot_not_reviewed_w_empties/"

im_list = os.listdir(im_src)
an_list = [x.replace("xml", "jpg") for x in os.listdir(an_src)]
list(set(im_list) - set(an_list))
list(set(an_list) - set(im_list))

if not os.path.exists(im_dst):
    os.mkdir(im_dst)

if not os.path.exists(an_dst):
    os.mkdir(an_dst)

slicer = ibis.Slicer()

# Options
slicer.keep_partial_labels == True
slicer.ignore_empty_tiles == False
slicer.save_before_after_map == True

slicer.config_dirs(img_src=im_src, ann_src=an_src, img_dst=im_dst, ann_dst=an_dst)

# Slice images and annotations
slicer.slice_by_size(tile_size=(1024,1024), tile_overlap=0.0, empty_sample=1.0)

# Slice images only
#slicer.slice_images_by_size((tile_size==(1024,1024), tile_overlap == 0.0))

#slicer.slice_by_size(tile_size=(1024,1024), tile_overlap=0.0, empty_sample= 0.0)
