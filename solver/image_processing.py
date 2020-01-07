import numpy as np
import operator
import cv2

def findcontour_version(img):
    """ This function changed in later versions. This enables compatibility"""
    major = cv2.__version__.split('.')[0]
    if major == '3':
        ret, contours, hierarchy = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours, hierarchy, ret
    else:
        contours, hierarchy = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours, hierarchy

def split_image(img):
    """ Split the image in to 81 cells which will then be read to identify the number or if blank"""
    cells = []
    side = img.shape[:1]
    side = side[0] / 9
    for i in range(9):
        for j in range(9):
            p1 = (i * side, j * side)              # Top left corner of the individual cell
            p2 = ((i + 1) * side, (j + 1) * side)  # Bottom right corner of the individual cell
            cells.append((p1, p2))


    # Displays the grid over the image
    for rect in cells:
        img = cv2.rectangle(img, tuple(int(x) for x in rect[0]), tuple(int(x) for x in rect[1]), 255)

    return img

def contour_corners(img, original):
    """ Assigns variables to the corners of the contoured puzzle. This will later be used to warp the
    image so it can better recognize them from an angle"""
    contours, hierarchy = findcontour_version(img)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)  # Sort by area, descending
    polygon = contours[0]  # Largest image
    key = operator.itemgetter(1)

    # Finds the coordinates to the four corners to the grid
    top_left, _ = min(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=key)
    top_rght, _ = max(enumerate([pt[0][0] - pt[0][1] for pt in polygon]), key=key)
    bot_rght, _ = max(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=key)
    bot_left, _ = min(enumerate([pt[0][0] - pt[0][1] for pt in polygon]), key=key)

    width, height = 450, 450

    # 1: the coordinates from the original image; 2: the coordinates to be placed in the new window
    corner1 = np.float32([[polygon[top_left][0]], [polygon[top_rght][0]],
                          [polygon[bot_left][0]], [polygon[bot_rght][0]]])
    corner2 = np.float32([[0,0], [width,0], [0,height], [width,height]])

    matrix = cv2.getPerspectiveTransform(corner1, corner2)
    output = cv2.warpPerspective(original, matrix, (width,height))

    for x in range(4):
        cv2.circle(img, (corner1[x][0][0], corner1[x][0][1]), 5, (0,0,255), cv2.FILLED)

    return output

def contour_image(img):
    """For some reason for version 3 they changed how contours worked (and changed it back afterwards)"""
    contours, hierarchy = findcontour_version(img)

    gray = img
    max_area = 0
    best_cnt = []
    c = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 1000:
            if area > max_area:
                max_area = area
                best_cnt = i
                img = cv2.drawContours(img, contours, c, (0, 255, 0), 2)
        c += 1

    mask = np.zeros(gray.shape, np.uint8)
    cv2.drawContours(mask, [best_cnt], 0, 255, -1)
    cv2.drawContours(mask, [best_cnt], 0, 0, 2)

    img = np.zeros_like(gray)
    img[mask == 255] = gray[mask == 255]

    # Makes the area outside main contour red
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    img = cv2.drawContours(img, contours, -1, (0, 0, 255), 3)

    return gray, img

def pre_process_image(img):
    """ Basic changes to the image"""
    # Gray scale:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Gaussian blur: reduces the noise that is picked up
    img = cv2.GaussianBlur(img, (5, 5), 0)

    # Adaptive threshold: Turns pixels black and white depending on the pixels around it
    # Binary threshold:   b/w pixels set to certain threshold. This isn't good for images with shadows
    img = cv2.adaptiveThreshold(img, 255, 1, 1, 11, 2)

    # Dilate:   Didn't really make a difference on the example image, but keeping here for now
    # img = cv2.dilate(img, kernel=np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], np.uint8), iterations=1)

    return img
