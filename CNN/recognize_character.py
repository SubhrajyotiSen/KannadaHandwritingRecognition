import cv2
import numpy as np
import tensorflow as tf
import os
from keras.models import load_model
from keras import backend as K

from CNN.ottakshara_dict import ottakshara_mapping


def keras_process_image(img):
    image_x, image_y = img.shape
    img = np.reshape(img, (1, image_x, image_y, 1))
    return img


def keras_predict(image, model):
    image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    processed = keras_process_image(image)
    pred_probab = list(model.predict(processed)[0])
    sorted_probab = sorted(pred_probab, reverse=True)
    return pred_probab.index(sorted_probab[0])


def recognize(dir):

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    tf.logging.set_verbosity(tf.logging.ERROR)

    # load the 2 models
    ottakshara_model = load_model('CNN/cnn_model_ottak.h5')
    char_model = load_model('CNN/cnn_model.h5')

    # dictionary to hold file names and their predictions
    predictions = {}

    # sort the list of image names alphabetically
    flist = os.listdir(dir)
    flist.sort()

    # iterate through each image and predict its class
    for file in flist:
        # if image is an ottakshara
        if '-1' in file:
            predictions[file] = ottakshara_mapping[keras_predict(
                os.path.abspath(os.path.join(dir, file)), ottakshara_model)]
        # if image in a regular character
        else:
            predictions[file] = keras_predict(
                os.path.abspath(os.path.join(dir, file)), char_model)

    K.clear_session()
    return predictions
