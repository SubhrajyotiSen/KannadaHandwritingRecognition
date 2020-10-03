import numpy as np
import pickle
import cv2
import os
import sys
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
from keras.optimizers import Adam
from keras.layers import LRN2D
from keras import backend as K
import matplotlib.pyplot as plt
import load_images
K.set_image_dim_ordering('tf')

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def get_image_size():
    img = cv2.imread(os.path.join(directory, '1', '1.jpg'), 0)
    return img.shape


def get_num_of_classes():
    return len(os.listdir(directory))


directory = sys.argv[1]
image_x, image_y = get_image_size()


def cnn_model():
    num_of_classes = get_num_of_classes()
    model = Sequential()
    model.add(Conv2D(52, (5, 5), input_shape=(
        image_x, image_y, 1), activation='tanh'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(LRN2D(alpha=0.1, beta=0.75))
    model.add(Conv2D(64, (5, 5), activation='tanh'))
    model.add(MaxPooling2D(pool_size=(5, 5), strides=(5, 5)))
    model.add(Flatten())
    model.add(Dropout(0.5))
    model.add(Dense(num_of_classes, activation='softmax'))
    sgd = optimizers.SGD(lr=1e-2)
    model.compile(loss='categorical_crossentropy', optimizer=Adam(
        lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0), metrics=['accuracy'])
    filepath = "cnn_model.h5"
    checkpoint1 = ModelCheckpoint(
        filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    callbacks_list = [checkpoint1]
    return model, callbacks_list


def train():
    with open("train_images", "rb") as f:
        train_images = np.array(pickle.load(f))
    with open("train_labels", "rb") as f:
        train_labels = np.array(pickle.load(f), dtype=np.int32)

    with open("test_images", "rb") as f:
        test_images = np.array(pickle.load(f))
    with open("test_labels", "rb") as f:
        test_labels = np.array(pickle.load(f), dtype=np.int32)

    train_images = np.reshape(
        train_images, (train_images.shape[0], image_x, image_y, 1))
    test_images = np.reshape(
        test_images, (test_images.shape[0], image_x, image_y, 1))
    train_labels = np_utils.to_categorical(train_labels)
    test_labels = np_utils.to_categorical(test_labels)

    model, callbacks_list = cnn_model()
    history = model.fit(train_images, train_labels, validation_data=(
        test_images, test_labels), epochs=100, batch_size=100, callbacks=callbacks_list)
    scores = model.evaluate(test_images, test_labels, verbose=0)
    print("CNN Error: %.2f%%" % (100-scores[1]*100))
    # summarize history for accuracy
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    # plt.show(hold=False)
    plt.savefig('acc.png')
    plt.clf()
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    # plt.show(hold=False)
    plt.savefig('loss.png')
    # model.save('cnn_model_keras2.h5')


# create the required datatset type from the images
load_images.create_pickle(directory)

train()
K.clear_session()
