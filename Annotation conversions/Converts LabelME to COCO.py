import labelme2coco

# Inputs: annot_dir = dir that contains labelme annotation files;
#  export_dir = dir to save newly formatted annotations
annot_dir = "C:/Users/bpickens/Desktop/testing/"
export_dir = "C:/Users/bpickens/Desktop/testing/new"

# convert labelme annotations to coco annotations
labelme2coco.convert(annot_dir, export_dir)