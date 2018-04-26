import cv2
import numpy as np
import tensorflow as tf
import os
import sys
from keras.models import load_model
from keras import backend as K

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.logging.set_verbosity(tf.logging.ERROR)
model = load_model('cnn_model.h5')

def get_image_size():
	img = cv2.imread(imageName, 0)
	return img.shape

imageName = sys.argv[1]
image_x, image_y = get_image_size()

def keras_process_image(img):
	print(img.shape)
	img = np.reshape(img, (1, image_x, image_y, 1))
	return img

def keras_predict(model, image):
	processed = keras_process_image(image)
	pred_probab = list(model.predict(processed)[0])
	sorted_probab = sorted(pred_probab, reverse=True)
	for x in sorted_probab[0:5]:
		print(x, pred_probab.index(x))

def recognize():
	image = cv2.imread(imageName, cv2.IMREAD_GRAYSCALE)
	keras_predict(model, image)
			

#keras_predict(model, np.zeros((28, 28), dtype=np.uint8))		
recognize()
K.clear_session();
