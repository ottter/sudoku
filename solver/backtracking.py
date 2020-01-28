import numpy as np

def build_array():
    # I imagine this will be used once I link it to the opencv portion
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
    # return np.zeros(shape=(9, 9))
    return puzzle_array

def is_empty(puzzle_array, cell):
    """Returns True is cell is empty; Returns False if cell is occupied"""
    if puzzle_array[cell[0]][cell[1]] == 0:
        return True
    return False

def is_valid(puzzle_array, cell, guess):
    """
    Returns True if puzzle is valid; Returns False if puzle is invalid
    - Checks if row of input cell is all unique values
    - Checks if column of input cell is all unique values
    - Checks if 3x3 square of input cell is all unique value"""
    col = []
    for x in range(9):
        col.append(puzzle_array[x][cell[1]])

    row = [value for value in puzzle_array[cell[0]].tolist() if value != 0]     # Removes empty cells
    col = [value for value in col if value != 0]

    col.append(guess)
    row.append(guess)

    if len(row) != len(set(row)):
        return False
    if len(col) != len(set(col)):
        return False

    box_x = cell[0] // 3    # Coordinates for 3x3 box the cell is in
    box_y = cell[1] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if puzzle_array[i][j] == guess:
                return False

    return True

def backtrack(puzzle_array):
    empty_cells = []    # Creates a list of positions with empty cells
    solved_array = puzzle_array
    for i in range(9):
        for j in range(9):
            if is_empty(solved_array, [i, j]) is True:
                empty_cells.append([i, j])

    for empty in empty_cells:
        for guess in range(1,10):
            if is_valid(solved_array, empty, guess) is True:
                solved_array[empty[0], empty[1]] = guess

                # TODO: Implement backtracking
    return solved_array

def solved():
    return

def main():
    puzzle_array = build_array()
    solved_array = backtrack(puzzle_array)
    print(solved_array)

if __name__ == "__main__":
    main()