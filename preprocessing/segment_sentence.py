import os
import cv2
import numpy as np


def segment_sentence(image, directory):

    line_dir = directory + "/lines"
    if not os.path.exists(line_dir):
        os.makedirs(line_dir)

    # grayscale the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # get threshold for pixel values
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    ret, thresh2 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # dilate the image
    kernel = np.ones((5, 100), np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)

    # find contours
    im2, ctrs, hier = cv2.findContours(
        img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # sort contours
    sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[1])
    sorted_ctrs = sorted_ctrs[0:]

    sentences = []

    for i, ctr in enumerate(sorted_ctrs):

        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)

        # Ignore small contours - Considered to be unwanted elements
        if ((w*h) < 5000):
            continue

        # Getting ROI
        roi = thresh2[y:y+h, x:x+w]

        # save each segmented image
        sentences.append(roi)

        cv2.imwrite(os.path.join(line_dir, str(i).zfill(2) + ".png"), roi)

    return sentences
