import numpy as np
import cv2
# https://medium.com/@neshpatel/solving-sudoku-part-ii-9a7019d196a2

PATH = './images/'

def findcontour_version(img):
    # This function changed in later versions. This enables compatibility
    major = cv2.__version__.split('.')[0]
    if major == '3':
        ret, contours, hierarchy = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours, hierarchy, ret
    else:
        contours, hierarchy = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours, hierarchy

def contour_image(img):
    # For some reason for version 3 they changed how contours worked (and changed it back afterwards)
    contours, hier = findcontour_version(img)

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

    # Working
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    img = cv2.drawContours(img, contours, -1, (0, 0, 255), 2)

    return img


def pre_process_image(img):
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

def main():
    # Import the image file with the sudoku puzzle
    img = cv2.imread(f'{PATH}sudoku-cropped.jpg')
    img = pre_process_image(img)
    img = contour_image(img)

    # Display the image & holds it open
    cv2.imshow('Sudoku', img)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()

# TODO: creates the grid for the puzzle
# TODO: warp mask image to be "front facing"
# TODO: number recognition in each cell
# TODO: backtracking solving algorithm
# TODO: real time reader via web cam
