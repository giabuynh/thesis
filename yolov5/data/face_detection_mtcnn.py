from matplotlib import pyplot
from matplotlib.patches import Rectangle, Circle
from mtcnn.mtcnn import MTCNN
# from facenet_pytorch import MTCNN
from PIL import Image, ImageDraw
import os
import numpy as np


def load_images_from_folder(folder_path):
	print('[INFO] Loading images from ', folder_path)
	filenames = os.listdir(folder_path)
	allowed_extension = ['jpg', 'png', 'jpeg', 'JPG', 'PNG', 'JPEG']
	images = []
	for filename in filenames:
		# get a full file path
		file_path = os.path.join(folder_path, filename)
		# check whether a file path is a file or a directory
		if os.path.isfile(file_path):
			# check whether a file is image file
			# try:
			# 	image = Image.open(file_path)
			# 	if image is not None:
			# 		images.append(filename)
			# 	image.close()
			# except:
			# 	continue
			filename_patterns = filename.split('.')
			if filename_patterns[-1] in allowed_extension:
				txt_filename = filename_patterns[0] + '.txt'
				if not txt_filename in filenames:
					images.append(filename)
	return images


def write_txt_files_from_dict(save_folder_path, info_dict):
	for file in info_dict:
		filename = file.split('.')[0]

		txt_file = open(save_folder_path + filename + '.txt', 'w')
		txt_file.write(info_dict[file])
		txt_file.close()


def write_txt_file(save_folder_path, image_filename, content):
	filename = image_filename.split('.')[0]
	print('	[WRITE]', filename + '.txt')

	txt_file = open(save_folder_path + filename + '.txt', 'w')
	txt_file.write(content)
	txt_file.close()


def detect_bounding_boxes_yolo_format(image_set_path, label):
	# load images from folder
	image_set = load_images_from_folder(image_set_path)
	cnt = 0

	# create the detector, using default weights
	print('[INFO] Load detector...')
	detector = MTCNN()
	print('[INFO] Detecting bounding boxes...')

	# annotation_dict = {}
	for image_filename in image_set:
		# get a full file path
		file_path = os.path.join(image_set_path, image_filename)
		cnt += 1

		# get image shape (height, width, channels)
		print('	[INFO] Open', image_filename + '. (' + str(cnt) + '/' + str(len(image_set)) + ')')
		image = pyplot.imread(file_path)
		image_h = image.shape[0]
		image_w = image.shape[1]
		# image_h, image_w, image_c = image.shape

		try:
			# detect faces in image
			faces = detector.detect_faces(image)

			# if len(faces) == 0:
			# 	annotation_dict[image_filename] = None
			annotations = ''

			for face in faces:
				# calculate bounding box
				x, y, w, h = face['box']  # x_left, y_bottom, width, height
				x = x + w / 2  # x_center
				y = y + h / 2  # y_center

				# normalize the co-ordinates by the dimensions of the image
				x /= image_w
				y /= image_h
				w /= image_w
				h /= image_h

				# if image_filename in annotation_dict:
				# 	annotation_dict[image_filename] += '\n' + label + ' ' + str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h)
				# else:
				# 	annotation_dict[image_filename] = label + ' ' + str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h)
				if len(annotations) == 0:
					annotations += label + ' ' + str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h)
				else:
					annotations += '\n' + label + ' ' + str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h)

			# create txt file in the same folder
			write_txt_file(image_set_path, image_filename, annotations)
		except:
			print('	[ERROR] Cannot detect image', image_filename, 'due to incompatible shape.')

	# create txt files
	# print('[INFO] Creating txt files...')
	# write_txt_files_from_dict(image_set_path, annotation_dict)
	# print('[INFO] Done.')

	# return annotation_dict


# Draw an image with detected objects
def draw_image_with_boxes_mtcnn_format(filename, result_list):
	# load the image
	data = pyplot.imread(filename)
	# plot the image
	pyplot.imshow(data)
	# get the context for drawing boxes
	ax = pyplot.gca()
	# plot each box
	for result in result_list:
		# get coordinates
		x, y, width, height = result['box']
		# create the shape
		rect = Rectangle((x, y), width, height, fill=False, color='red')
		dot = Circle((x, y), radius=2, color='green')
		# draw the box
		ax.add_patch(rect)
		ax.add_patch(dot)
	# show the plot
	pyplot.show()


def draw_image_with_boxes_yolo_format(image_file, txt_file):
    image = Image.open(image_file)
    w, h = image.size

    annotation_file = open(txt_file, 'r')
    annotation_list = annotation_file.read().split('\n')
    annotation_list = [x.split(' ') for x in annotation_list]
    annotation_list = [[float(y) for y in x] for x in annotation_list]

    annotations = np.array(annotation_list)

    plotted_image = ImageDraw.Draw(image)

    transformed_annotations = np.copy(annotations)
    transformed_annotations[:, [1, 3]] = annotations[:, [1, 3]] * w
    transformed_annotations[:, [2, 4]] = annotations[:, [2, 4]] * h

    transformed_annotations[:, 1] = transformed_annotations[:, 1] - (transformed_annotations[:, 3] / 2)
    transformed_annotations[:, 2] = transformed_annotations[:, 2] - (transformed_annotations[:, 4] / 2)
    transformed_annotations[:, 3] = transformed_annotations[:, 1] + transformed_annotations[:, 3]
    transformed_annotations[:, 4] = transformed_annotations[:, 2] + transformed_annotations[:, 4]

    for ann in transformed_annotations:
        obj_cls, x0, y0, x1, y1 = ann
        border_width = 3
        plotted_image.rectangle(((x0, y0), (x1, y1)), outline=(255, 0, 0), width=border_width)

    pyplot.imshow(np.array(image))
    pyplot.show()


# Prepare images
image_set_path = 'D:/Thesis/MyData/Frames/mask_weared_incorrect/'
# annotation_dict =
detect_bounding_boxes_yolo_format(image_set_path, 'mask_weared_incorrect')
# print('[COMPLETE] Detected bounding boxes')

# for image_filename in annotation_dict:
# 	image_filename_patterns = image_filename.split('.')
# 	txt_filename = image_filename_patterns[0] + '.txt'
# 	draw_image_with_boxes_yolo_format(os.path.join(image_set_path, image_filename), os.path.join(image_set_path, txt_filename))
