import xml.etree.ElementTree as ET
import os
import json
import pandas as pd

xml_path = 'C:/Users/aware/Desktop/tile_annot_not_reviewed'
json_file = 'C:/users/aware/desktop/crazy.json'

final_csv = "C:/Users/aware/desktop/converted_voc_to_csv.csv"
filename = json_file

#l1 = os.listdir(xml_path)
#print(l1)

coco = dict()
coco['images'] = []
coco['type'] = 'instances'
coco['annotations'] = []
coco['categories'] = []

category_set = dict()
image_set = set()

category_item_id = 0
image_id = 0
annotation_id = 0

def addCatItem(name):
    global category_item_id
    category_item = dict()
    category_item['supercategory'] = 'none'
    category_item_id += 1
    category_item['id'] = category_item_id
    category_item['name'] = name
    coco['categories'].append(category_item)
    category_set[name] = category_item_id
    return category_item_id


def addImgItem(file_name, size):
    global image_id
    if file_name is None:
        raise Exception('Could not find filename tag in xml file.')
    if size['width'] is None:
        raise Exception('Could not find width tag in xml file.')
    if size['height'] is None:
        raise Exception('Could not find height tag in xml file.')
    image_id += 1
    image_item = dict()
    image_item['id'] = image_id
    image_item['file_name'] = file_name
    image_item['width'] = size['width']
    image_item['height'] = size['height']
    coco['images'].append(image_item)
    image_set.add(file_name)
    return image_id


def addAnnoItem(object_name, image_id, category_id, bbox):
    global annotation_id
    annotation_item = dict()
    annotation_item['segmentation'] = []
    seg = []
    # bbox[] is x,y,w,h
    # left_top
    seg.append(bbox[0])
    seg.append(bbox[1])
    # left_bottom
    seg.append(bbox[0])
    seg.append(bbox[1] + bbox[3])
    # right_bottom
    seg.append(bbox[0] + bbox[2])
    seg.append(bbox[1] + bbox[3])
    # right_top
    seg.append(bbox[0] + bbox[2])
    seg.append(bbox[1])

    annotation_item['segmentation'].append(seg)

    annotation_item['area'] = bbox[2] * bbox[3]
    annotation_item['iscrowd'] = 0
    annotation_item['ignore'] = 0
    annotation_item['image_id'] = image_id
    annotation_item['bbox'] = bbox
    annotation_item['category_id'] = category_id
    annotation_id += 1
    annotation_item['id'] = annotation_id
    coco['annotations'].append(annotation_item)

def parseXmlFiles(xml_path):
    for f in os.listdir(xml_path):
        print("okay")
#        if not f.endswith('.xml'):
 #           continue

        bndbox = dict()
        size = dict()
        current_image_id = None
        current_category_id = None
        file_name = None
        size['width'] = None
        size['height'] = None
        size['depth'] = None

        xml_file = os.path.join(xml_path, f)
        print(xml_file)

        tree = ET.parse(xml_file)
        root = tree.getroot()
        if root.tag != 'annotation':
            raise Exception('pascal voc xml root element should be annotation, rather than {}'.format(root.tag))

        # elem is <folder>, <filename>, <size>, <object>
        for elem in root:
            current_parent = elem.tag
            current_sub = None
            object_name = None

            if elem.tag == 'folder':
                continue

            if elem.tag == 'filename':
                file_name = elem.text
                if file_name in category_set:
                    raise Exception('file_name duplicated')

            # add img item only after parse <size> tag
            elif current_image_id is None and file_name is not None and size['width'] is not None:
                if file_name not in image_set:
                    current_image_id = addImgItem(file_name, size)
                    print('add image with {} and {}'.format(file_name, size))
                else:
                    raise Exception('duplicated image: {}'.format(file_name))
                    # subelem is <width>, <height>, <depth>, <name>, <bndbox>
            for subelem in elem:
                bndbox['xmin'] = None
                bndbox['xmax'] = None
                bndbox['ymin'] = None
                bndbox['ymax'] = None

                current_sub = subelem.tag
                if current_parent == 'object' and subelem.tag == 'name':
                    object_name = subelem.text
                    if object_name not in category_set:
                        current_category_id = addCatItem(object_name)
                    else:
                        current_category_id = category_set[object_name]

                elif current_parent == 'size':
                    if size[subelem.tag] is not None:
                        raise Exception('xml structure broken at size tag.')
                    size[subelem.tag] = int(subelem.text)

                # option is <xmin>, <ymin>, <xmax>, <ymax>, when subelem is <bndbox>
                for option in subelem:
                    if current_sub == 'bndbox':
                        if bndbox[option.tag] is not None:
                            raise Exception('xml structure corrupted at bndbox tag.')
                        bndbox[option.tag] = int(option.text)

                # only after parse the <object> tag
                if bndbox['xmin'] is not None:
                    if object_name is None:
                        raise Exception('xml structure broken at bndbox tag')
                    if current_image_id is None:
                        raise Exception('xml structure broken at bndbox tag')
                    if current_category_id is None:
                        raise Exception('xml structure broken at bndbox tag')
                    bbox = []
                    # x
                    bbox.append(bndbox['xmin'])
                    # y
                    bbox.append(bndbox['ymin'])
                    # w
                    bbox.append(bndbox['xmax'] - bndbox['xmin'])
                    # h
                    bbox.append(bndbox['ymax'] - bndbox['ymin'])
                    print('add annotation with {},{},{},{}'.format(object_name, current_image_id, current_category_id,
                                                                   bbox))
                    addAnnoItem(object_name, current_image_id, current_category_id, bbox)


if __name__ == '__main__':
    print("LKJL")
 #   xml_path = 'Annotations'
    parseXmlFiles(xml_path)
    json.dump(coco, open(json_file, 'w'))


### STEP 1- EXPORT ANNOTATION DATA
# Outputs annotation data and image id index number
def convert_coco_json_to_csv(filename):
    js = json.load(open(filename, 'r'))  # read & parse JSON string and convert it to a Python Dictionary
    out_file = filename[:-5]
    out = open(out_file + '_json_data_to_CSV.csv', 'w')  # open for writing to file
    out.write('image_id, x_min,y_min,w,h,label_id \n')  #

    all_ids = []
    for im in js['images']:
        all_ids.append(im['file_name'])

    all_ids_ann = []
    for ann in js['annotations']:
        image_id = ann['image_id']
        # print(image_id)
        all_ids_ann.append(image_id)
        label_id = ann['category_id']
        all_ids_ann.append(label_id)
        #  print(label)
        x_min = ann['bbox'][0]
        #   print (x_min)
        all_ids_ann.append(x_min)
        y_min = ann['bbox'][1]
        all_ids_ann.append(y_min)
        w = ann['bbox'][2]
        all_ids_ann.append(w)
        h = ann['bbox'][3]
        all_ids_ann.append(h)

        out.write('{},{},{},{},{},{}\n'.format(image_id, x_min, y_min, w, h, label_id))

    all_ids = set(all_ids)
    all_ids_ann = set(all_ids_ann)
    no_annotations = list(all_ids - all_ids_ann)
    out.close()

## STEP 2- EXPORT CSV WITH IMAGE NAMES, IMAGE ID NUMBERS
def convert_coco_names_to_csv(csv_file):
    s = json.load(open(filename, 'r'))  # read & parse JSON string and convert it to a Python Dictionary
    out_file = filename[:-5]
    out2 = open(out_file + '_names_toCSV.csv', 'w')  # open for writing to file
    out2.write('image_id, unique_image_jpg \n')  #

    all_data = []
    for ann in s['images']:
        id = ann['id']
        # print (id)
        all_data.append(id)
        unique_image_jpg = ann['file_name']
        #  print(unique_image_jpg)
        all_data.append(unique_image_jpg)
        out2.write('{},{} \n'.format(id, unique_image_jpg))

# Run functions to get 2 csv files
convert_coco_json_to_csv(filename)
convert_coco_names_to_csv(filename)

# Read in; 1st, Erase extra image names at end of "data to csv" file
prefix = filename[:-5]
csv_names= ("".join([prefix,"_names_toCSV.csv"]))
csv_data = ("".join([prefix,"_json_data_to_CSV.csv"]))

csv_names = pd.read_csv(csv_names)
csv_data = pd.read_csv(csv_data)

# Merge
merge1 = csv_data.merge(csv_names, left_on= 'image_id', right_on = 'image_id' )
print (merge1)
merge1.to_csv(final_csv, index=False)
