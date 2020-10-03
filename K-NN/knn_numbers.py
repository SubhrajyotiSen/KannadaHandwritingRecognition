
import numpy as np
import cv2 as cv

# for displaying the whole numpy array
np.set_printoptions(threshold=np.nan)

img = cv.imread(r'final.jpg', 0)
#gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
# Now we split the image to 50x10 cells, each 52x52 size
cells = [np.hsplit(row, 50) for row in np.vsplit(img, 10)]
# Make it into a Numpy array.
x = np.array(cells)
# Now we prepare train_data and test_data.
train = x[:, :25].reshape(-1, 2704).astype(np.float32)
test = x[:, 25:50].reshape(-1, 2704).astype(np.float32)

# Create labels for train and test data
k = np.arange(10)  # 10 because 10 number to classify
train_labels = np.repeat(k, 25)[:, np.newaxis]
test_labels = train_labels.copy()

# Initiate kNN, train the data, then test it with test data for k=1
knn = cv.ml.KNearest_create()
knn.train(train, cv.ml.ROW_SAMPLE, train_labels)

ret, result, neighbours, dist = knn.findNearest(test, k=5)

# Now we check the accuracy of classification
# For that, compare the result with test_labels and check which are wrong

matches = result == test_labels
correct = np.count_nonzero(matches)
accuracy = correct*100.0/result.size
print(accuracy)

# we store the train numpy array for further use
np.savez('knn_data.npz', train=train, train_labels=train_labels)

# Now load the data
with np.load('knn_data.npz') as data:
    print(data.files)
    train = data['train']
    train_labels = data['train_labels']
    print(train)
