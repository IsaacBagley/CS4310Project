from random import sample, choice
import time


def generate_random_board(blank_squares):
    # Function to generate a random Sudoku board
    base = 3
    side = base * base

    # Generate the indices for rows/columns/numbers
    rows = [g * base + r for g in range(base) for r in range(base)]
    cols = [g * base + c for g in range(base) for c in range(base)]
    nums = sample(range(1, base * base + 1), base * base)

    # Create the complete Sudoku board based on the pattern
    board = [[nums[generate_pattern(base, side, r, c)] for c in cols] for r in rows]

    # Create an incomplete Sudoku board by removing some cells
    blanks_generated = 0
    while blanks_generated < blank_squares:
        row, col = choice(range(side)), choice(range(side))
        if board[row][col] != 0:
            board[row][col] = 0
            blanks_generated += 1

    return board


def input_board():
    print("Enter the initial Sudoku board:")
    board = []
    for i in range(9):
        row = input(f"Enter row {i + 1} (9 numbers separated by spaces, use '0' for empty cells): ").strip().split()
        if len(row) != 9 or not all(cell.isdigit() and 0 <= int(cell) <= 9 for cell in row):
            print("Invalid input. Please enter 9 numbers separated by spaces.")
            return None
        board.append([int(cell) for cell in row])
    return board


def generate_pattern(base, side, r, c):
    # Generate a complete Sudoku board pattern
    return (base * (r % base) + r // base + c) % side


def find_empty_location(board):
    # Find the first empty (zero) cell
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j

    # No empty cell found
    return None, None


def is_valid(board, row, col, num):
    # Check if the number is not present in the current row/column
    if num in board[row] or num in [board[i][col] for i in range(9)]:
        return False

    # Check if the number is not present in the current 3x3 sub-grid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    if any(num in board[i][start_col:start_col + 3] for i in range(start_row, start_row + 3)):
        return False

    return True


def forward_checking(board, row, col, num):
    # Save current values
    saved_values = []

    # Eliminate the possibility of "num" in the same row/column
    for i in range(9):
        if board[row][i] == 0 and num not in board[row]:
            saved_values.append((row, i, board[row][i]))
            board[row][i] = 0
        if board[i][col] == 0 and i != row and board[i][col] == num:
            saved_values.append((i, col, board[i][col]))
            board[i][col] = 0

    # Eliminate the possibility of "num" in the same 3x3 sub-grid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == 0 and num not in [board[x][y] for x in
                                                                        range(start_row, start_row + 3) for y in
                                                                        range(start_col, start_col + 3)]:
                saved_values.append((start_row + i, start_col + j, board[start_row + i][start_col + j]))
                board[start_row + i][start_col + j] = 0

    return saved_values


def undo_forward_checking(board, saved_values):
    # Undo forward checking for backtracking
    for i, j, value in saved_values:
        board[i][j] = value


def solve_sudoku(board):
    # Find the first (next) empty cell
    empty_row, empty_col = find_empty_location(board)

    if empty_row is None:
        # No empty cell, puzzle is solved
        return True

    # Try numbers from 1 to 9
    for num in range(1, 10):
        if is_valid(board, empty_row, empty_col, num):
            # Check if the current cell is empty in the original puzzle
            if board[empty_row][empty_col] == 0:
                # Try placing the number in the empty cell
                board[empty_row][empty_col] = num

                # Apply forward checking
                saved_values = forward_checking(board, empty_row, empty_col, num)

                # Recursively solve the rest of the puzzle
                if solve_sudoku(board):
                    return True

                # If the current placement produces an invalid solution, backtrack
                board[empty_row][empty_col] = 0

                # Undo forward checking
                undo_forward_checking(board, saved_values)
            else:
                # If the current cell is not empty in the original puzzle, skip it
                if solve_sudoku(board):
                    return True

    # No valid number found for this cell; backtrack
    return False


def print_board(board):
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j, num in enumerate(row):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(num, end=" ")
        print()


if __name__ == "__main__":
    answer = input("Would you like to input your own board? (yes/no): ")
    if answer.lower() == "no":
        clues = int(input("How many clues are used? "))
        blanks = 81 - clues
        board = generate_random_board(blanks)
        print("Initial Board:")
        print_board(board)
    else:
        board = input_board()
        if board is None:
            exit()  # Exit if the input is invalid
    start = time.process_time_ns()
    print("\nSolving...\n")
    if solve_sudoku(board):
        print("Solved Board:")
        print_board(board)
        end = time.process_time_ns() - start
        print("Time to solve =", end/1000, "us")
    else:
        print("No solution found.")
        end = time.process_time_ns() - start
        print("Time to not find solution =", end/1000, "us")
