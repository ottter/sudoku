import numpy as np

def build_array():
    # I imagine this will be used once I link it to the opencv portion
    return np.zeros(shape=(9, 9))

def is_empty():
    """Check if the cell is empty"""
    return

def is_valid():
    """Check if the box and row/col is valid"""
    return

def backtrack():
    """Algorithm TBD"""
    return

def main():
    # Temporary input until I connect this portion to opencv
    puzzle_array = np.array([[2, 3, 0, 4, 1, 5, 0, 6, 8],
                             [0, 8, 0, 2, 3, 6, 5, 1, 9],
                             [1, 6, 0, 9, 8, 7, 2, 3, 4],
                             [3, 1, 7, 0, 9, 4, 0, 2, 5],
                             [4, 5, 8, 1, 2, 0, 6, 9, 7],
                             [9, 2, 6, 0, 5, 8, 3, 0, 1],
                             [0, 0, 0, 5, 0, 0, 1, 0, 2],
                             [0, 0, 0, 8, 4, 2, 9, 0, 3],
                             [5, 9, 2, 3, 7, 1, 4, 8, 6]])

    print(puzzle_array.shape)

if __name__ == "__main__":
    main()