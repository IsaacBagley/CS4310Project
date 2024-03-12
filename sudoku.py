from random import sample, choice
import PySimpleGUI as sg


def generate_random_board():
    # Function to illustrate the program's viability with any given Sudoku puzzle
    base = 3
    side = base * base

    # Generate the indices for rows/columns/numbers
    rows = [g * base + r for g in range(base) for r in range(base)]
    cols = [g * base + c for g in range(base) for c in range(base)]
    nums = sample(range(1, base * base + 1), base * base)

    # Create the complete Sudoku board based on the pattern
    board = [[nums[generate_pattern(base, side, r, c)] for c in cols] for r in rows]

    # Create an incomplete Sudoku board by removing some cells
    for _ in range(side * side // 2):
        row, col = choice(range(side)), choice(range(side))
        board[row][col] = 0

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


def solve_sudoku(board, window):
    # Find the first (next) empty cell
    empty_row, empty_col = find_empty_location(board)

    if empty_row is None:
        # No empty cell, puzzle is solved
        return True

    for num in range(1, 10):
        if is_valid(board, empty_row, empty_col, num):
            # Try placing the number in the empty cell
            board[empty_row][empty_col] = num

            # Apply forward checking
            saved_values = forward_checking(board, empty_row, empty_col, num)

            # Update GUI
            window[empty_row, empty_col].update(num)

            # Recursively solve the rest of the puzzle
            if solve_sudoku(board, window):
                return True

            # If the current placement produces an invalid solution, backtrack
            board[empty_row][empty_col] = 0

            # Undo forward checking
            undo_forward_checking(board, saved_values)
            window[empty_row, empty_col].update("")

    # No valid number found for this cell; backtrack
    return False


def sudoku_solver_gui(board):
    # Define the layout for the Sudoku board
    sg.theme("Default1")

    # Create 9x9 grid
    layout = []

    # Create rows and layouts for the 3x3 sub-grids
    for i in range(3):
        row = []
        for j in range(3):
            subgrid_layout = []
            # Define the layout for each cell within the sub-grid as a single text element
            for m in range(3):
                cell_row = []
                for n in range(3):
                    cell_layout = [
                        [sg.Text("", size=(1, 1), pad=(0, 0), justification="center", key=(3 * i + m, 3 * j + n))],
                    ]
                    # Create a border around each cell
                    cell_row.append(sg.Frame("", cell_layout, relief="ridge"))
                # Add the row of cells to the sub-grid layout
                subgrid_layout.append(cell_row)
            # Add the sub-grid layout to the row
            row.append(sg.Frame("", subgrid_layout, relief="ridge"))
        # Add the row of sub-grids to the overall layout
        layout.append(row)

    # Add "Solve" and "Quit" buttons
    layout.append([sg.Button("Solve"), sg.Button("Quit")])

    # Create the GUI window
    window = sg.Window("Sudoku Solver", layout, finalize=True)

    # Initialize the given board
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                window[(i, j)].update(board[i][j], text_color="blue")

    # Event loop
    while True:
        event, values = window.read()

        # Handle window close or "Quit" button click
        if event == sg.WINDOW_CLOSED or event == "Quit":
            break

        # Handle "Solve" button click
        if event == "Solve":
            if solve_sudoku(board, window):
                # Update input fields with solved Sudoku values
                for i in range(9):
                    for j in range(9):
                        window[i, j].update(board[i][j], text_color="blue")
            else:
                sg.popup("No solution found.")

    window.close()


if __name__ == "__main__":
    # # Generate a random Sudoku board
    # board = generate_random_board()

    # If this voodoo frightens you, use the given example board instead
    board = [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0],
    ]
    sudoku_solver_gui(board)
