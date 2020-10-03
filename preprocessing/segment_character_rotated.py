import cv2
import numpy as np
import os
import sys

# Rotate, Crop and Save images


def getSubImage(rect, src):
    center, size, theta = rect
    # Get the angle of rotation for each contour(character)
    # Use it fot further processing and slant angle estimation
    print(theta)
    center, size = tuple(map(int, center)), tuple(map(int, size))
    # Get rotation matrix for rectangle
    M = cv2.getRotationMatrix2D(center, theta, 1)
    # Perform rotation on src image
    dst = cv2.warpAffine(src, M, src.shape[:2])
    out = cv2.getRectSubPix(dst, size, center)
    # Save the output
    cv2.imwrite(os.path.join(newfolder, 'segment' + str(i) + '.png'), out)


if __name__ == '__main__':
    imageName = sys.argv[1]
    # Creating new folder to save the preprocessed images
    fileName = filename = os.path.splitext(imageName)[0]
    folder = "Segmented_rtdChar_" + filename

    newfolder = os.path.join(os.getcwd(), folder)
    if not os.path.exists(newfolder):  # Check if subfolder already exists
        os.makedirs(newfolder)
    image = cv2.imread(imageName)
    cv2.imshow("original", image)
    cv2.waitKey(0)

    # Convert to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("gray",gray)
    # cv2.waitKey(0)

    # binary
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow('thresh', thresh)
    cv2.waitKey(0)

    # find contours
    im2, ctrs, hier = cv2.findContours(
        thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # sort contours
    sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])

    for i, ctr in enumerate(sorted_ctrs):
        # Get bounding box
        rect = cv2.minAreaRect(ctr)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(image, [box], 0, (255, 255, 255), 0)
        getSubImage(rect, image)

    # cv2.imshow('final image with boxes',image)
    # cv2.waitKey(0)
