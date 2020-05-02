from solver.image_processing import pre_process_image, contour_image, contour_corners, split_image
from solver.backtracking import solve_sudoku
import cv2

PATH_TO_IMAGES = './images/'


def main():
    original = cv2.imread(PATH_TO_IMAGES + 'sudoku-2.jpg')      # Import the image file with the sudoku puzzle
    # cv2.imshow('Original', original)

    processed_image = pre_process_image(original)               # Gray-scale, Gaussian blur, Adaptive threshold

    contoured_image, contoured_color = contour_image(processed_image) # Finds the outer sides of the puzzle grid

    warped_image = contour_corners(contoured_image, original)   # Crops background & warps the image for birds-eye view

    squared_image = split_image(warped_image)                    # Splits the image in to 81 cells

    cv2.imshow('puzzle', squared_image)                          # Visualization

    solve_sudoku()                                               # Solves the puzzle using the given array

    cv2.waitKey(0)                                               # Holds the visualization open

if __name__ == "__main__":
    main()

# TODO: individual cell recognition
# TODO: number recognition in each cell
# TODO: backtracking solving algorithm
# TODO: real time reader via web cam