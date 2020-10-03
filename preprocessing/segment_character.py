import cv2

""" To sort the contours in 4 ways
		left-to-right
		right-to-left
		top-to-bottom
		bottom-to-top
"""


def sort_contours(cnts, method="left-to-right"):
    # initialize the reverse flag and sort index
    reverse = False
    i = 0

    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True

    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1

    # construct the list of bounding boxes and sort them from top to bottom
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))

    # return the list of sorted contours and bounding boxes
    return (cnts, boundingBoxes)


def segment_character(image, directory):

    row, col = image.shape

    ret, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
    ret, thresh2 = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    im2, ctrs, hier = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    (ctrs, boundingBoxes) = sort_contours(ctrs, method="left-to-right")

    characters = {}
    ottaksharas = {}

    count = 0

    # For each contour, find the bounding rectangle and draw it
    for i, cnt in enumerate(ctrs):
        x, y, w, h = cv2.boundingRect(cnt)

        # Ignore small contours - Considered to be unwanted elements
        if ((w*h) < 100):
            continue

        # Find the segmented character and store
        roi = thresh2[y:y+h, x:x+w]

        # Analyse the contour bounding box x,y,h,w values to get better understanding

        """
			Ottakshara is always present at bottom when compared with rest of the characters in the word.

			Hence when we draw contours, the contours of ottaksharas begin at a height lesser than
			50% of the total height of the image.
			(We are making an assumption of 50% here which works well most of the time)
 
			Based on above condition, store the roi accordingly into character and ottakshara dictionaries
 
			character dictionary
				char_contour_id: roi
 
			ottakshara dictionary
				parent_char_contour_id: roi
			where parent_char_contour_id maps to char_contour_id of character dictionary
 
			This works well in case only one ottakshara is present for each character.
 
			TODO:
					Make method more efficient and make it possible to map multiple ottaksharas belonging to one parent character
					How?
					Map ottakshara to character based on x values now.
					compare ottakshara(x) and every character(x+h) values and map to closest character



		"""
        if(y > (row/2)):
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 1)
            ottaksharas[count-1] = roi
        else:
            characters[count] = roi
            count = count + 1

    return characters, ottaksharas
