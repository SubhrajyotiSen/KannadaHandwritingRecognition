"""
    TO EXECUTE SCRIPT

    python svm_predict.py testfolder N file

    testfolder - The folder containing the test images
    N - Number of classes present
    file - File to load the trained model. The file type should be ".dat"

    example - 
                python svm_predict.py test 10 modelsave.dat

"""


import cv2
import glob
import numpy as np
import os
import sys

SZ = 52
CLASS_N = int(sys.argv[2])
matchcount = 0
mismatchcount = 0

def deskew(img):
    m = cv2.moments(img)
    if abs(m['mu02']) < 1e-2:
        return img.copy()
    skew = m['mu11']/m['mu02']
    M = np.float32([[1, skew, -0.5*SZ*skew], [0, 1, 0]])
    img = cv2.warpAffine(img, M, (SZ, SZ), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR)
    return img

def get_hog() : 
    winSize = (52,52)
    blockSize = (8,8)
    blockStride = (4,4)
    cellSize = (8,8)
    nbins = 9
    derivAperture = 1
    winSigma = -1.
    histogramNormType = 0
    L2HysThreshold = 0.2
    gammaCorrection = 1
    nlevels = 64
    signedGradient = True

    hog = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nbins,derivAperture,winSigma,histogramNormType,L2HysThreshold,gammaCorrection,nlevels, signedGradient)

    return hog
    affine_flags = cv2.WARP_INVERSE_MAP|cv2.INTER_LINEAR

def svmPredict(model, samples):
    return model.predict(samples)[1].ravel()

# Increase matchcount if match was found
def match():
    global matchcount 
    matchcount = matchcount + 1
    return
# Increase mismatchcount if mismatch was found
def mismatch():
    global mismatchcount    
    mismatchcount = mismatchcount + 1
    return

def testmyModel():
	hog = get_hog()
	modelsave = sys.argv[3]
	model = cv2.ml.SVM_load(modelsave)
	test_path = sys.argv[1]
	for folder in os.listdir(test_path):
		print("\n##############  ", folder, "  ##############")
		hog_descriptors = []
		for file in os.listdir(os.path.join(test_path,folder)):
			img_predict = cv2.imread(os.path.join(test_path, folder, file),0)
			hog_descriptors.append(hog.compute(deskew(img_predict)))	
		hog_descriptors = np.squeeze(hog_descriptors)
		prediction = svmPredict(model,hog_descriptors)
		x = len(prediction)	
		for i in range(x):
			if(int(prediction[i])==int(folder)):
				#print("Match",": ", "---", "prediction", ": ", prediction[i])
				match()
			else:
				mismatch()
				print("MissMatch",": ", file, "---", "prediction", ": ", prediction[i])
	print("===================================================")
	print("number of mismatches:",mismatchcount)
	print("number of matches:",matchcount)
	totalfiles=mismatchcount+matchcount
	acc=(matchcount/totalfiles)*100
	print("total number of letters:",totalfiles)
	print("accuracy:",'%.2f'%acc,"%")

testmyModel()