import numpy as np
import cv2
import math
from heapq import nlargest
from matplotlib import pyplot as plt

# Find minimum x value


def findxi(thin_image, row, col):
    xi = 0
    for i in range(1, row-1):
        for j in range(1, col-1):
            if(thin_image[i][j] == 1):
                xi = i
                return xi

# Find maximum x value


def findxm(thin_image, row, col):
    xm = 0
    for i in range(1, row-1):
        for j in range(1, col-1):
            if(thin_image[i][j] == 1):
                if(i > xm):
                    xm = i
    return xm

# Plot original and new image for comparison


def showImage(image, newImage):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(8, 4),
                             sharex=True, sharey=True,
                             subplot_kw={'adjustable': 'box-forced'})

    ax = axes.ravel()

    ax[0].imshow(image, cmap=plt.cm.gray)
    ax[0].axis('off')
    ax[0].set_title('original', fontsize=20)

    ax[1].imshow(newImage, cmap=plt.cm.gray)
    ax[1].axis('off')
    ax[1].set_title('newImage', fontsize=20)

    fig.tight_layout()
    plt.show()

# The vertical projection profile of an image that has highest intensity will be considered as the output


def verticalProjection(img):
    r, c = img.shape
    rows = []
    sums = []
    for i in range(r-1):
        count = 0
        for j in range(c-1):
            if(img[i][j] == 1):
                count = count+1
        print(i, count)
        rows.append(i)
        sums.append(count)
    print(nlargest(5, sums))  # Find peaks, not max 5 values
    plt.ylim(1, 100)
    plt.xlim(1, r-1)
    plt.plot(rows, sums, color='green')
    plt.show()

# For the foreground pixels, calculate new x and y values, store new image in new_image


def removeSlant(thin_image, theta, row, col):
    new_image = np.zeros([2000, 2000])
    for i in range(1, row-1):
        for j in range(1, col-1):
            if(thin_image[i][j] == 1):
                dx = i+j*(theta*0.01)
                delx = int(dx)
                new_image[delx][j] = 1
    # Saving output image
    # im = toimage(new_image)
    # im.save("slantised.png")
    verticalProjection(new_image)
    # Show the image
    showImage(thin_image, new_image)
    # cv2.imshow("afterslant", new_image)
    # cv2.waitKey(0)


imageName = sys.argv[1]
image = cv2.imread(imageName)  # Image path

# Make copy of the image so that original image is not lost
thin_image = image.copy()
row, col = thin_image.shape
print(row, col)
xi = findxi(thin_image, row, col)
xm = findxm(thin_image, row, col)
print(xi)
print(xm)
val = (1.5*(xm+xi))/(xm-xi)
print(val)
# math.degrees to convert radians to degrees
theta = math.degrees(math.atan(val))
print(theta)
minusTheta = math.degrees(math.atan(-val))
print(minusTheta)
verticalProjection(image)
removeSlant(image, theta, row, col)
removeSlant(image, minusTheta, row, col)
