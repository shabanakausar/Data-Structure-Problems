"""
Sudoku Solver — Backtracking Algorithm
=======================================
The board is a 9x9 list of lists.
Use 0 to represent empty cells.
"""


def is_valid(board, row, col, num):
    """
    Check whether placing `num` at board[row][col] is legal.
    A move is legal if `num` does not already appear in:
      - the same row
      - the same column
      - the same 3x3 box
    """
    # Check the row
    if num in board[row]:
        return False

    # Check the column
    if num in [board[r][col] for r in range(9)]:
        return False

    # Check the 3x3 box
    # Find the top-left corner of the box this cell belongs to
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if board[r][c] == num:
                return False

    return True


def find_empty(board):
    """
    Scan the board left-to-right, top-to-bottom.
    Return (row, col) of the first empty cell (value 0),
    or None if the board is completely filled.
    """
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return (row, col)
    return None


def solve(board):
    """
    Attempt to solve the board in-place using backtracking.
    Returns True if solved, False if no solution exists.

    Algorithm:
      1. Find an empty cell.
      2. If none found → puzzle is solved, return True.
      3. Try digits 1–9 in that cell.
      4. If a digit is valid, place it and recurse.
      5. If recursion succeeds → return True (propagate success).
      6. If recursion fails → erase the digit (backtrack) and try next.
      7. If no digit works → return False (trigger backtrack in caller).
    """
    empty = find_empty(board)

    # Base case: no empty cells left — puzzle solved
    if not empty:
        return True

    row, col = empty

    for num in range(1, 10):           # Try digits 1 through 9
        if is_valid(board, row, col, num):
            board[row][col] = num      # Place the digit (tentative)

            if solve(board):           # Recurse on the rest of the board
                return True            # Propagate success upward

            board[row][col] = 0        # Backtrack: erase and try next digit

    return False                       # No digit worked → backtrack further


def print_board(board):
    """Pretty-print the 9x9 board with box separators."""
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("------+-------+------")
        row_str = ""
        for j, val in enumerate(row):
            if j % 3 == 0 and j != 0:
                row_str += "| "
            row_str += (str(val) if val != 0 else ".") + " "
        print(row_str)


# ── Example puzzle (0 = empty cell) ──────────────────────────────────────────
puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

print("Puzzle:")
print_board(puzzle)
print()

if solve(puzzle):
    print("Solution:")
    print_board(puzzle)
else:
    print("No solution exists.")