empty_cells = []    # Format: [x, y, answer]    Purpose: potentially for opencv output

def build_array():
    sudoku = [[2, 3, 0, 4, 1, 5, 0, 6, 8],
              [0, 8, 0, 2, 3, 6, 5, 1, 9],
              [1, 6, 0, 9, 8, 7, 2, 3, 4],
              [3, 1, 7, 0, 9, 4, 0, 2, 5],
              [4, 5, 8, 1, 2, 0, 6, 9, 7],
              [9, 2, 6, 0, 5, 8, 3, 0, 1],
              [0, 0, 0, 5, 0, 0, 1, 0, 2],
              [0, 0, 0, 8, 4, 2, 9, 0, 3],
              [5, 9, 2, 3, 7, 1, 4, 8, 6]]
    return sudoku

def print_sudoku(puzzle_array):
    for i in puzzle_array:
        print (i)

def is_empty(puzzle_array):
    # Checks for empty (0) cells, returns solved (True) or position of empty cell (False)
    for x in range(9):
        for y in range (9):
            if puzzle_array[x][y] == 0:
                row, col = x, y
                return [row, col, False]
    return [0, 0, True]

def is_safe(sudoku, guess, row, col):
    # Checks if guess is valid for row
    for i in range(9):
        if sudoku[i][col] == guess:
            return False
        if sudoku[row][i] == guess:
            return False

    box_x = row // 3 * 3   # Coordinates for 3x3 box the cell is in
    box_y = col // 3 * 3

    for x in range(box_x, box_x + 3):
        for y in range(box_y, box_y + 3):
            if sudoku[x][y] == guess:
                return False
    return True

def solve_sudoku(sudoku):
    solution = is_empty(sudoku)

    if solution[2]:
        return True
    row, col = solution[0], solution[1]

    for guess in range(1,10):
        if is_safe(sudoku, guess, row, col):
            sudoku[row][col] = guess
            if solve_sudoku(sudoku):
                empty_cells.append([solution[0], solution[1], guess])
                return True

            sudoku[row][col]=0
    return False

def main():
    sudoku = build_array()
    if solve_sudoku(sudoku):
        print_sudoku(sudoku)
    else:
        print("No solution")

if __name__ == "__main__":
    main()
