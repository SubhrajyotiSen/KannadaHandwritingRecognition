import cv2
import numpy as np
import tensorflow as tf
import os
import sys
from keras.models import load_model
from keras import backend as K

def init():
	os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
	tf.logging.set_verbosity(tf.logging.ERROR)

def keras_process_image(img):
	image_x, image_y = img.shape
	img = np.reshape(img, (1, image_x, image_y, 1))
	return img

def keras_predict(model, image):
	processed = keras_process_image(image)
	pred_probab = list(model.predict(processed)[0])
	sorted_probab = sorted(pred_probab, reverse=True)
	return pred_probab.index(sorted_probab[0])

def recognize(imageName,flag):
	init()
	if flag == 'ottakshara':
		model = load_model('CNN/cnn_model_ottak.h5')
	else:
		model = load_model('CNN/cnn_model.h5')
	image = cv2.imread(imageName, cv2.IMREAD_GRAYSCALE)
	prediction = keras_predict(model, image)
	K.clear_session();
	return prediction