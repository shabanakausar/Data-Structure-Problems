# Data-Structure-Problems
The Core Idea
Imagine filling the grid like a maze. You walk forward placing numbers, and when you hit a dead end (a contradiction), you back up to the last decision and try a different number.
# Sudoku Solver — Backtracking Algorithm

A clean, well-commented implementation of a Sudoku solver using the **backtracking** algorithm, available in Python, JavaScript, and C++. Given any valid puzzle, it finds the unique solution in milliseconds.

---

## Table of contents

- [How it works](#how-it-works)
- [Project structure](#project-structure)
- [Board format](#board-format)
- [Code walkthrough](#code-walkthrough)
  - [is_valid — the constraint checker](#1-is_valid--the-constraint-checker)
  - [find_empty — the cell scanner](#2-find_empty--the-cell-scanner)
  - [solve — the backtracking engine](#3-solve--the-backtracking-engine)
  - [print_board — pretty printer](#4-print_board--pretty-printer)
- [Running the code](#running-the-code)
- [Example output](#example-output)
- [Complexity](#complexity)
- [Languages](#languages)

---

## How it works

Backtracking is a **depth-first search with pruning**. The algorithm walks through every empty cell one by one and:

1. Tries placing digits `1` through `9`.
2. Immediately checks if the digit is valid (not already in the same row, column, or 3×3 box).
3. If valid, places the digit and **recurses** into the next empty cell.
4. If the recursion reaches a dead end, it **erases** the digit and tries the next one.
5. If no digit works, it returns `False` — signalling the caller to backtrack too.

This continues until either every cell is filled (puzzle solved) or all possibilities are exhausted (no solution).

```
Find empty cell
      │
      ▼
  None found? ──► Solved ✓
      │
      ▼
Try digits 1–9
      │
   Valid? ──No──► Try next digit
      │
     Yes
      │
      ▼
  Place digit
  Recurse ──► Succeeded? ──Yes──► Return True ✓
      │
      No
      │
      ▼
  Erase digit  ◄── Backtrack
```

---

## Project structure

```
sudoku-solver/
├── sudoku_solver.py      # Python implementation
├── sudoku_solver.js      # JavaScript implementation
├── sudoku_solver.cpp     # C++ implementation
└── README.md
```

---

## Board format

The board is represented as a **9×9 grid** (list of lists in Python, array of arrays in JS, 2D array in C++).

- **Given clues** are stored as integers `1–9`.
- **Empty cells** are stored as `0`.

```python
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
```

---

## Code walkthrough

The solver is built from four focused functions. Each does exactly one job.

---

### 1. `is_valid` — the constraint checker

```python
def is_valid(board, row, col, num):
    # Check the row
    if num in board[row]:
        return False

    # Check the column
    if num in [board[r][col] for r in range(9)]:
        return False

    # Check the 3x3 box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if board[r][c] == num:
                return False

    return True
```

**What it does:** Before placing any digit, this function enforces the three Sudoku rules.

**Row check** — `num in board[row]` scans the entire row. If the number is already there, placement is illegal.

**Column check** — builds a list of all values in column `col` across every row and checks for `num`.

**Box check** — this is the trickiest part. Integer division `(row // 3) * 3` snaps any row index to the top-left corner of its 3×3 box:

| Cell row | `row // 3` | `* 3` = box start |
|----------|------------|-------------------|
| 0, 1, 2  | 0          | 0                 |
| 3, 4, 5  | 1          | 3                 |
| 6, 7, 8  | 2          | 6                 |

The same formula works for columns. It then loops through the 3×3 area and checks for conflicts.

**Returns:** `True` if placement is safe, `False` if it violates any rule.

---

### 2. `find_empty` — the cell scanner

```python
def find_empty(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return (row, col)
    return None
```

**What it does:** Scans the board left-to-right, top-to-bottom and returns the coordinates of the first empty cell (`0`).

**Returns:** A `(row, col)` tuple if an empty cell exists, or `None` if the board is fully filled — which is the **base case** that tells `solve()` the puzzle is complete.

> **Design note:** Scanning top-left first is the simplest strategy. More advanced solvers use *minimum remaining values (MRV)* — picking the cell with the fewest valid candidates first — to reduce the search tree significantly. For a standard 9×9 puzzle the simple scan is fast enough.

---

### 3. `solve` — the backtracking engine

```python
def solve(board):
    empty = find_empty(board)

    # Base case: board is full → solved
    if not empty:
        return True

    row, col = empty

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num       # 1. Place

            if solve(board):            # 2. Recurse
                return True             # 3. Propagate success

            board[row][col] = 0         # 4. Backtrack

    return False                        # 5. No digit worked
```

**What it does:** This is the core of the algorithm. It is a **recursive function** — it calls itself to fill the next cell after placing a digit.

The five numbered lines are the entire backtracking pattern:

| Step | Line | Meaning |
|------|------|---------|
| 1 | `board[row][col] = num` | Tentatively place the digit |
| 2 | `if solve(board)` | Try to solve the rest of the board |
| 3 | `return True` | If it worked, propagate success all the way up |
| 4 | `board[row][col] = 0` | If it failed, erase the digit |
| 5 | `return False` | Signal the caller that this path is a dead end |

**Why `board[row][col] = 0` is the key line:** This single erasure is "backtracking". By undoing the placement, the board is restored to exactly the state it was in before this call — so the caller can try the next digit cleanly. No copies of the board are ever made; mutation + erasure achieves the same result with far less memory.

**Base case:** When `find_empty` returns `None`, there are no empty cells left. The board is full and valid (every placement was checked before it was made), so the function returns `True`.

---

### 4. `print_board` — pretty printer

```python
def print_board(board):
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("------+-------+------")
        row_str = ""
        for j, val in enumerate(row):
            if j % 3 == 0 and j != 0:
                row_str += "| "
            row_str += (str(val) if val != 0 else ".") + " "
        print(row_str)
```

**What it does:** Formats the board for terminal output. Prints a separator line `------+-------+------` every three rows (but not before row 0) and a `|` divider every three columns, producing the familiar Sudoku grid layout. Empty cells (`0`) are shown as `.` for readability.

---

## Running the code

**Python** (requires Python 3.6+)

```bash
python sudoku_solver.py
```

**JavaScript** (requires Node.js)

```bash
node sudoku_solver.js
```

**C++** (requires a C++11-compatible compiler)

```bash
g++ -std=c++11 -o sudoku_solver sudoku_solver.cpp
./sudoku_solver
```

---

## Example output

```
Puzzle:
5 3 . | . 7 . | . . .
6 . . | 1 9 5 | . . .
. 9 8 | . . . | . 6 .
------+-------+------
8 . . | . 6 . | . . 3
4 . . | 8 . 3 | . . 1
7 . . | . 2 . | . . 6
------+-------+------
. 6 . | . . . | 2 8 .
. . . | 4 1 9 | . . 5
. . . | . 8 . | . 7 9

Solution:
5 3 4 | 6 7 8 | 9 1 2
6 7 2 | 1 9 5 | 3 4 8
1 9 8 | 3 4 2 | 5 6 7
------+-------+------
8 5 9 | 7 6 1 | 4 2 3
4 2 6 | 8 5 3 | 7 9 1
7 1 3 | 9 2 4 | 8 5 6
------+-------+------
9 6 1 | 5 3 7 | 2 8 4
2 8 7 | 4 1 9 | 6 3 5
3 4 5 | 2 8 6 | 1 7 9
```

---

## Complexity

| | Value |
|---|---|
| Time (worst case) | O(9^m) where m = number of empty cells |
| Space | O(m) recursion stack depth |
| Typical solve time | < 1 ms for a standard 9×9 puzzle |

The worst-case bound sounds large, but the `is_valid` check prunes the vast majority of branches before they are explored. In practice the algorithm is extremely fast on all published 9×9 puzzles.

---

## Languages

| File | Language | Run with |
|------|----------|----------|
| `sudoku_solver.py` | Python 3 | `python sudoku_solver.py` |
