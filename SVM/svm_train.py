"""
    TO EXECUTE SCRIPT

    svm_train("train_image", no_of_classes, trained_model_file)

    train_image - Mnist image with all the characters. Size of each character in image is 52x52 pixels
    no_of_classes - Number of classes present
        1. 34 if you are training with ottaksharas
        2. 52 for letters
        3. 10 for numbers
    trained_model_file - The trained model that can be saved for testing accuracy and predictions. This generated dat file is to be fed to prediction script.
           The file type should be ".dat"

    example -
                svm_train("test.jpg", 10, "digits.dat")

    UNCOMMENT THE FUNCTION CALL AT THE END OF THE SCRIPT AS PER USECASE

    Once uncommented, run script using following command -

    - python3 svm_train.py

    Important - You need python 3.x to run the script

"""


#!/usr/bin/env python
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Size of each image
SZ = 52
# No of classes present
CLASS_N = 0
c_accuracy_set = []

# Split the images into cells based on SZ which is 52*52


def split2d(img, cell_size, flatten=True):
    h, w = img.shape[:2]
    sx, sy = cell_size
    cells = [np.hsplit(row, w//sx) for row in np.vsplit(img, h//sy)]
    cells = np.array(cells)
    if flatten:
        cells = cells.reshape(-1, sy, sx)
    return cells

# Load the image data, split and label them


def load_digits(fn):
    digits_img = cv2.imread(fn, 0)
    digits = split2d(digits_img, (SZ, SZ))
    labels = np.repeat(np.arange(CLASS_N), len(digits)/CLASS_N)
    return digits, labels

# deskew image


def deskew(img):
    m = cv2.moments(img)
    if abs(m['mu02']) < 1e-2:
        return img.copy()
    skew = m['mu11']/m['mu02']
    M = np.float32([[1, skew, -0.5*SZ*skew], [0, 1, 0]])
    img = cv2.warpAffine(
        img, M, (SZ, SZ), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR)
    return img

# SVM initialisation
# C=12.5, gamma=0.001


def svmInit(C, gamma):
    model = cv2.ml.SVM_create()
    model.setGamma(gamma)
    model.setC(C)
    model.setKernel(cv2.ml.SVM_RBF)
    model.setType(cv2.ml.SVM_C_SVC)
    return model


def svmTrain(model, samples, responses):
    model.train(samples, cv2.ml.ROW_SAMPLE, responses)
    return model


def svmPredict(model, samples):
    return model.predict(samples)[1].ravel()

# Evaluate trained model. Print Accuracy obtained during validation


def svmEvaluate(model, digits, samples, labels):
    predictions = svmPredict(model, samples)
    accuracy = (labels == predictions).mean()
    print('Percentage Accuracy: %.2f %%' % (accuracy*100))

# Histogram of Oriented Gradients is used as feature set.
# Below provides initialisation of HOG


def get_hog():
    winSize = (52, 52)
    blockSize = (8, 8)
    blockStride = (4, 4)
    cellSize = (8, 8)
    nbins = 9
    derivAperture = 1
    winSigma = -1.
    histogramNormType = 0
    L2HysThreshold = 0.2
    gammaCorrection = 1
    nlevels = 64
    signedGradient = True

    hog = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins, derivAperture,
                            winSigma, histogramNormType, L2HysThreshold, gammaCorrection, nlevels, signedGradient)

    return hog
    affine_flags = cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR


def svm_train(imageName, no_of_classes, modelsave):

    global CLASS_N
    CLASS_N = no_of_classes
    digits, labels = load_digits(imageName)

    # Shuffle data
    rand = np.random.RandomState(10)
    shuffle = rand.permutation(len(digits))
    digits, labels = digits[shuffle], labels[shuffle]

    # Deskew images
    digits_deskewed = list(map(deskew, digits))

    # HoG feature descriptor
    hog = get_hog()

    # Calculate HOG descriptors for all the images
    hog_descriptors = []
    for img in digits_deskewed:
        hog_descriptors.append(hog.compute(img))
    hog_descriptors = np.squeeze(hog_descriptors)
    print(hog_descriptors.shape)

    # Spliting data into training (90%) and test set (10%)
    train_n = int(0.9*len(hog_descriptors))
    digits_train, digits_test = np.split(digits_deskewed, [train_n])
    hog_descriptors_train, hog_descriptors_test = np.split(
        hog_descriptors, [train_n])
    labels_train, labels_test = np.split(labels, [train_n])

    # Used to generate SVM Learning curve graph
    """for m in range(1,15,3):
        model = svmInit(m,0.001)
        svmTrain(model, hog_descriptors_train, labels_train)
        print('Evaluating model ... ')
        vis = svmEvaluate(model, digits_test, hog_descriptors_test, labels_test, m)
        print(m)"""

    # Train SVM Model
    model = svmInit(12.5, 0.001)
    svmTrain(model, hog_descriptors_train, labels_train)
    # Evaluate model
    vis = svmEvaluate(model, digits_test, hog_descriptors_test, labels_test)
    # Save model
    model.save(modelsave)
    cv2.destroyAllWindows()

# TODO: Uncomment the function call below while running script
# svm_train(train_image, no_of_classes, trained_model_file)
