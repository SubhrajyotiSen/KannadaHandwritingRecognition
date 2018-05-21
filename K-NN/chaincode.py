#---------------------------------------------------------------------------#
#------------CODE TO IMPLEMENT FREEMAN CHAIN CODE(8 neighbours)-------------#
#FOR REFERENCE REFER : http://www.cs.unca.edu/~reiser/imaging/chaincode.html#

import cv2
# Image path(replace with local image path)
image = cv2.imread(r'C:\...\oo.png', 0)
row, col = image.shape
print(row, col)
ret, img = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('image', img)
cv2.waitKey(1)

# Discover the first point
for i, row in enumerate(img):
    for j, value in enumerate(row):
        if value == 255:
            start_point = (i, j)
            print(start_point, value)
            break
    else:
        continue
    break

# assign the direction matrix
directions = [0,  1,  2,
              7,      3,
              6,  5,  4]
dir2idx = dict(zip(directions, range(len(directions))))


change_j = [-1,  0,  1,  # x or columns
            -1,      1,
            -1,  0,  1]

change_i = [-1, -1, -1,  # y or rows
            0,      0,
            1,  1,  1]

ch = []
border = []
chain = []
curr_point = start_point
histogram = [0, 0, 0, 0, 0, 0, 0, 0]

for direction in directions:
    idx = dir2idx[direction]
    new_point = (start_point[0] + change_i[idx],
                 start_point[1] + change_j[idx])
    if img[new_point] != 0:  # if is ROI
        border.append(new_point)
        chain.append(direction)
        curr_point = new_point
        break

count = 0
while curr_point != start_point:
    # figure direction to start search
    b_direction = (direction + 5) % 8
    dirs_1 = range(b_direction, 8)
    dirs_2 = range(0, b_direction)
    dirs = []
    dirs.extend(dirs_1)
    dirs.extend(dirs_2)
    for direction in dirs:
        idx = dir2idx[direction]
        new_point = (curr_point[0] + change_i[idx],
                     curr_point[1] + change_j[idx])
        if image[new_point] != 0:  # if is ROI
            border.append(new_point)
            chain.append(direction)
            curr_point = new_point
            break
    if count == 1000:
        break
    count += 1
# count contains the number of elements in the code
print(count)
print(" ")

# chain contains the chaincode for the letter
print(chain)
for i in range(0, count):
    a = chain[i]
    histogram[a] += 1

# prepare histogram and find percentage
for i in range(0, 8):
    histogram[i] = (histogram[i]/count)*100
for i in range(0, 8):
    print(histogram[i])
