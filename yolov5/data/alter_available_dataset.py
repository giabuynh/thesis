import os
import re
import shutil
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt


# def format_xml_ibug_to_yolo(xml_file):
#     root = ET.parse(xml_file).getroot()
#     info_dict = dict()
#     MIRROR = re.compile("_mirror")
#     ORIGINAL = re.compile("_1.")
#
#     for child in root:
#         if child.tag == 'images':
#             root = child
#
#     for child in root:
#         # Get location of the file
#         link_to_file = child.attrib['file']
#         link_patterns = link_to_file.split('/')
#
#         if re.findall(MIRROR, link_patterns[-1]) or not re.findall(ORIGINAL, link_patterns[-1]):
#             continue
#
#         if link_patterns[0] != 'afw':
#             break
#
#         # Create content of txt file
#         for subchild in child:
#             top = int(subchild.attrib['top'])
#             left = int(subchild.attrib['left'])
#             width = int(subchild.attrib['width'])
#             height = int(subchild.attrib['height'])
#
#             # Calculate bounding box
#             b_x_center = left + width / 2
#             b_y_center = top + height / 2
#             b_width = width
#             b_height = height
#
#             # Normalize the co-ordinates by the dimensions of the image
#             # image = cv2.imread(dataset_path + link_to_file)
#             # h, w, c = image.shape
#             image = Image.open(dataset_path + link_to_file)
#             w, h = image.size
#             b_x_center /= w
#             b_y_center /= h
#             b_width /= w
#             b_height /= h
#
#             tmp = "10 " + str(b_x_center)
#             tmp += " " + str(b_y_center)
#             tmp += " " + str(b_width)
#             tmp += " " + str(b_height)
#
#         if link_to_file in info_dict:
#             info_dict[link_to_file] += "\n" + tmp
#         else:
#             info_dict[link_to_file] = tmp
#
#     return info_dict


def filt_ibug_300W_image(xml_file):
    root = ET.parse(xml_file).getroot()
    images_files = []
    MIRROR = re.compile("_mirror")
    MASKED = re.compile("_masked")
    DASH_ONE_DOT = re.compile("_1.")
    DASH_ZERO_ONE_DOT = re.compile("_01.")

    for child in root:
        if child.tag == 'images':
            root = child

    for child in root:
        # Get location of the file
        link_to_file = child.attrib['file']
        link_patterns = link_to_file.split('/')

        if re.findall(MIRROR, link_patterns[-1]) or re.findall(MASKED, link_patterns[-1]):
            continue

        if re.findall(DASH_ONE_DOT, link_patterns[-1]) or re.findall(DASH_ZERO_ONE_DOT, link_patterns[-1]):
            images_files.append(link_to_file)
        else:
            file_name_patterns = link_patterns[-1].split('_')
            if file_name_patterns[-2] == 'image' or link_patterns[0] == 'helen':
                images_files.append(link_to_file)

    return images_files

def ibug300W():
    # Copy sum file
    dataset_path = "D:/NCM/ibug_300W_large_face_landmark_dataset/"
    xml_file = dataset_path + "labels_ibug_300W.xml"
    output_dataset_path = "D:/Thesis/MyData/ibug300W/"

    images_files = filt_ibug_300W_image(xml_file)
    print(images_files)
    for link_to_file in images_files:
        # Copy image file to the output folder
        shutil.copy2(dataset_path + link_to_file, output_dataset_path)


def HongNhuNgoc_change_labels():
    dataset_label_path = 'D:/Thesis/MyData/HongNhuNgoc/labels/'
    filenames = os.listdir(dataset_label_path)
    for filename in filenames:
        file = open(os.path.join(dataset_label_path, filename), 'r')
        lines = file.readlines()
        file.close()

        file = open(os.path.join(dataset_label_path, filename), 'w')
        for i in range(len(lines)):
            line_patterns = lines[i].split(' ')
            if line_patterns[0] == '0':
                line_patterns[0] = 'with_mask'
            else:
                line_patterns[0] = 'without_mask'
            lines[i] = ' '.join(line_patterns)

        new_lines = ''.join(lines)
        file.write(new_lines)
        file.close()


# HongNhuNgoc_change_labels()


def Masked_Wearing_v1():
    dataset_label_path = 'D:/Thesis/MyData/Mask Wearing.v1-416x416-black-padding.yolov5pytorch/labels/'
    filenames = os.listdir(dataset_label_path)
    for filename in filenames:
        file = open(os.path.join(dataset_label_path, filename), 'r')
        lines = file.readlines()
        file.close()

        file = open(os.path.join(dataset_label_path, filename), 'w')
        for i in range(len(lines)):
            line_patterns = lines[i].split(' ')
            if line_patterns[0] == '0':
                line_patterns[0] = 'with_mask'
            else:
                line_patterns[0] = 'without_mask'
            lines[i] = ' '.join(line_patterns)

        new_lines = ''.join(lines)
        file.write(new_lines)
        file.close()


# Masked_Wearing_v1()


# def build_folder(info_dict):
#     for link_to_file in info_dict:
#         # Copy image file to the output folder
#         shutil.copy2(dataset_path + link_to_file, output_dataset_path)
#
#         # Get image name
#         link_patterns = link_to_file.split('/')
#         file_name = link_patterns[-1].split('.')
#
#         # Create txt file
#         txt_file = open(output_dataset_path + file_name[0] + '.txt', 'w')
#         txt_file.write(info_dict[link_to_file])
#         txt_file.close()
#     print('[INFO] Copied')


# class_name_to_id_mapping = {"trafficlight": 0,
#                            "stop": 1,
#                            "speedlimit": 2,
#                            "newborn": 10}
# class_id_to_name_mapping = dict(zip(class_name_to_id_mapping.values(), class_name_to_id_mapping.keys()))

# def test_annotation_box(image_file, txt_file):
#     image = Image.open(image_file)
#     w, h = image.size
#
#     annotation_file = open(txt_file, 'r')
#     annotation_list = annotation_file.read().split("\n")
#     annotation_list = [x.split(" ") for x in annotation_list]
#     annotation_list = [[float(y) for y in x] for x in annotation_list]
#
#     annotations = np.array(annotation_list)
#
#     plotted_image = ImageDraw.Draw(image)
#
#     transformed_annotations = np.copy(annotations)
#     transformed_annotations[:, [1, 3]] = annotations[:, [1, 3]] * w
#     transformed_annotations[:, [2, 4]] = annotations[:, [2, 4]] * h
#
#     transformed_annotations[:, 1] = transformed_annotations[:, 1] - (transformed_annotations[:, 3] / 2)
#     transformed_annotations[:, 2] = transformed_annotations[:, 2] - (transformed_annotations[:, 4] / 2)
#     transformed_annotations[:, 3] = transformed_annotations[:, 1] + transformed_annotations[:, 3]
#     transformed_annotations[:, 4] = transformed_annotations[:, 2] + transformed_annotations[:, 4]
#
#     for ann in transformed_annotations:
#         obj_cls, x0, y0, x1, y1 = ann
#         border_width = 3
#         plotted_image.rectangle(((x0, y0), (x1, y1)), outline=(255, 0, 0), width=border_width)
#
#         # plotted_image.text((x0, y0 - 10), class_id_to_name_mapping[(int(obj_cls))])
#
#     plt.imshow(np.array(image))
#     plt.show()


# test_annotation_box('images/train/maksssksksss0_png.rf.7dc211c6e6af49bb921c1c65cf5b8f4e.jpg',
#                     'labels/train/maksssksksss0_png.rf.7dc211c6e6af49bb921c1c65cf5b8f4e.txt')
# test_annotation_box('../../MyData/ibug300W/1051618982_1.jpg', '../../MyData/ibug300W/1051618982_1.txt')
# test_annotation_box('../../MyData/ibug300W/3729198156_1.jpg', '../../MyData/ibug300W/3729198156_1.txt')
# test_annotation_box('../../MyData/ibug300W/134212_1.jpg', '../../MyData/ibug300W/134212_1.txt')
