'''
Author: EvilPort2

'''

# TODO: Documentation

import cv2
import os
import numpy as np
from sklearn.utils import shuffle
import pickle


def pickle_images_labels(image_dir):
    images_labels = []
    images = []
    labels = []
    for g_id in os.listdir(image_dir):
        for i in range(1200):
            img = cv2.imread(image_dir+"/"+g_id+"/"+str(i+1)+".jpg", 0)
            if np.any(img == None):
                continue
            images_labels.append((np.array(img, dtype=np.float32), int(g_id)))
    return images_labels


def split_images_labels(images_labels):
    images = []
    labels = []
    for (image, label) in images_labels:
        images.append(image)
        labels.append(label)
    return images, labels


def create_pickle(image_dir):

    images_labels = pickle_images_labels(image_dir)
    images_labels = shuffle(shuffle(shuffle(images_labels)))
    images, labels = split_images_labels(images_labels)
    print("Length of images_labels", len(images_labels))

    train_images = images[:int(5/6*len(images))]
    print("Length of train_images", len(train_images))
    with open("train_images", "wb") as f:
        pickle.dump(train_images, f)
    del train_images

    train_labels = labels[:int(5/6*len(labels))]
    print("Length of train_labels", len(train_labels))
    with open("train_labels", "wb") as f:
        pickle.dump(train_labels, f)
    del train_labels

    test_images = images[int(5/6*len(images)):]
    print("Length of test_images", len(test_images))
    with open("test_images", "wb") as f:
        pickle.dump(test_images, f)
    del test_images

    test_labels = labels[int(5/6*len(labels)):]
    print("Length of test_labels", len(test_labels))
    with open("test_labels", "wb") as f:
        pickle.dump(test_labels, f)
    del test_labels
