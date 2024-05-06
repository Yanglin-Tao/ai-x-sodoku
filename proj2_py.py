# Import necessary libaries
import pandas as pd
import altair as alt

# Reads input file
def read_input_file(file_path):
    try:
        matrix = []
        with open(file_path, 'r') as file:
            for line in file:
                row = list(map(int, line.strip().split()))
                matrix.append(row)
        return matrix
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Prompts user for input file name
file_path = input("Please enter the path to the input Sudoku file: ")
try:
    sudoku_matrix = read_input_file(file_path)
    for row in sudoku_matrix:
        print(row)
except Exception as e:
    print(f"Error: {e}")

# Create visualization of the unsolved sodoku matrix
def matrix_to_dataframe(matrix):
    data = {
        'row': [],
        'col': [],
        'value': []
    }
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            data['row'].append(i + 1)
            data['col'].append(j + 1)
            data['value'].append(value)
    return pd.DataFrame(data)

df = matrix_to_dataframe(sudoku_matrix)

chart = alt.Chart(df).mark_text(size=20).encode(
    x=alt.X('col:O', axis=alt.Axis(title=None, labels=False)),
    y=alt.Y('row:O', axis=alt.Axis(title=None, labels=False)),
    text='value:N',
    color=alt.condition(
        alt.datum.value == 0, 
        alt.value('lightgray'),  
        alt.value('black')      
    )
).properties(
    width=300,
    height=300
)

rules = alt.Chart(pd.DataFrame({'position': [3.5, 6.5]})).mark_rule(color='white', strokeWidth=2).encode(
    x='position:O', 
    y='position:O' 
)

chart = chart + rules
chart

# Find next unassigned variable in the sodoku matrix
def select_unassigned_variable(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None

# Check whether the assignment is consistent with CSP constraints
def is_consistent(board, row, col, num):
    block_row, block_col = 3 * (row // 3), 3 * (col // 3)
    # Check row and column constraints
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    # Check block constraint
    for i in range(3):
        for j in range(3):
            if board[block_row + i][block_col + j] == num:
                return False
    # Check main diagonal constraint
    if row == col:
        for i in range(9):
            if board[i][i] == num:
                return False
    # Check anti-diagonal constraint
    if row + col == 8:
        for i in range(9):
            if board[i][8-i] == num:
                return False
    return True

# Implement backtracking algorithm
def backtrack(board):
    # Find next unassigned variable
    unassigned = select_unassigned_variable(board)
    # If all variables are assigned, return
    if not unassigned:
        return True  
    
    row, col = unassigned
    
    # Loop domain values
    for num in range(1, 10):
        # Check whether the value is consistent with constraints
        if is_consistent(board, row, col, num):
            board[row][col] = num
            if backtrack(board):
                return True
            # Backtrack
            board[row][col] = 0
    return False


# Write to an output file
def write_output_file(matrix, file_path):
    with open(file_path, 'w') as file:
        for row in matrix:
            file.write(" ".join(map(str, row)) + "\n")

# Checks if the sodoku has been solved
if backtrack(sudoku_matrix):
    write_output_file(sudoku_matrix, "Output3.txt")
else:
    print("No solution exists")

# Create visualization of the solved sodoku matrix
df = matrix_to_dataframe(sudoku_matrix)

chart = alt.Chart(df).mark_text(size=20).encode(
    x=alt.X('col:O', axis=alt.Axis(title=None, labels=False)),
    y=alt.Y('row:O', axis=alt.Axis(title=None, labels=False)),
    text='value:N',
    color=alt.condition(
        alt.datum.value == 0, 
        alt.value('lightgray'),  
        alt.value('black')      
    )
).properties(
    width=300,
    height=300
)

rules = alt.Chart(pd.DataFrame({'position': [3.5, 6.5]})).mark_rule(color='white', strokeWidth=2).encode(
    x='position:O', 
    y='position:O' 
)


chart = chart + rules
chart
