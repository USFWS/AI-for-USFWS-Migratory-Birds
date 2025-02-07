import os
import torch
import image_bbox_tiler as ibis

#os.chdir("E:/a_detection_of_seabirds/new_tiles_test1")
## error in Main.py, line 273 is good;  line 300-305 is issue

# im_src = image source, an_src = annotation source
im_src = "C:/Brad/a_detection_of_seabirds/hive_images_not_reviewed"
an_src = "C:/Brad/a_detection_of_seabirds/hive_annot_not_reviewed/"

# error is below
#os.listdir('E:\\detection_of_seabirds\\demo_parents\\C1_L1_F10_T20230621_132003_892\\')
#os.listdir ('E:/detection_of_seabirds/demo_parents')

# Enter destination
im_dst = "C:/Brad/a_detection_of_seabirds/tiles_not_reviewed_w_empties/"
an_dst = "C:/Brad/a_detection_of_seabirds/tile_annot_not_reviewed_w_empties/"

print("ok")
im_list = os.listdir(im_src)
an_list = [x.replace("xml", "jpg") for x in os.listdir(an_src)]
list(set(im_list) - set(an_list))
list(set(an_list) - set(im_list))

#os.mkdir(im_dst)
#os.mkdir(an_dst)

slicer = ibis.Slicer()
slicer.config_dirs(img_src=im_src, ann_src=an_src, img_dst=im_dst, ann_dst=an_dst)

slicer.keep_partial_labels == True
slicer.ignore_empty_tiles == False
slicer.save_before_after_map == True

# Slice images and annotations
slicer.slice_by_size(tile_size=(1024,1024), tile_overlap=0.0, empty_sample=1.0)

# Slice images only
#slicer.slice_images_by_size((tile_size==(1024,1024), tile_overlap == 0.0))


#slicer.slice_by_size(tile_size=(1024,1024), tile_overlap=0.0, empty_sample= 0.0)