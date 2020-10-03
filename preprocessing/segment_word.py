import os
import cv2
import numpy as np


def segment_word(image, directory, count):

    word_dir = directory + "/words"
    if not os.path.exists(word_dir):
        os.makedirs(word_dir)
    # get threshold for pixel values
    ret, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
    ret, thresh2 = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    # dilate the image
    kernel = np.ones((5, 40), np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)

    # find contours
    im2, ctrs, hier = cv2.findContours(
        img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # sort contours
    sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
    sorted_ctrs = sorted_ctrs[0:]

    words = []

    for i, ctr in enumerate(sorted_ctrs):

        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)

        # Used to remove stray elements
        if ((w*h) < 1000):
            continue

        # Getting ROI
        roi = thresh2[y:y+h, x:x+w]

        # add each segmented image to list
        words.append(roi)
        cv2.imwrite(os.path.join(word_dir, str(count).zfill(
            2) + "-" + str(i).zfill(2) + ".png"), roi)

    return words
