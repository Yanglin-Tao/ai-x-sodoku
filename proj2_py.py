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
    min_options = float('inf')
    best_cell = None
    best_degree = -1
    
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                options = find_options(board, row, col)
                num_options = len(options)
                if num_options < min_options:
                    min_options = num_options
                    best_cell = (row, col, options)
                    best_degree = calculate_degree(board, row, col)
                elif num_options == min_options:
                    current_degree = calculate_degree(board, row, col)
                    if current_degree > best_degree:
                        best_cell = (row, col, options)
                        best_degree = current_degree
    
    return best_cell

def find_options(board, row, col):
    options = set(range(1, 10))
    block_row, block_col = 3 * (row // 3), 3 * (col // 3)

    # Remove options based on row, column, and block
    for i in range(9):
        options.discard(board[row][i])
        options.discard(board[i][col])
        options.discard(board[block_row + i//3][block_col + i%3])

    # Remove options based on diagonals if applicable
    if row == col:
        for i in range(9):
            options.discard(board[i][i])
    if row + col == 8:
        for i in range(9):
            options.discard(board[i][8-i])

    return options

def calculate_degree(board, row, col):
    degree = 0
    for i in range(9):
        if board[row][i] == 0:
            degree += 1
        if board[i][col] == 0:
            degree += 1
        # Check cells in the same block
        block_row = 3 * (row // 3)
        block_col = 3 * (col // 3)
        start_row = block_row + (i // 3)
        start_col = block_col + (i % 3)
        if board[start_row][start_col] == 0:
            degree += 1
    if row == col:
        for i in range(9):
            if board[i][i] == 0:
                degree += 1
    if row + col == 8:
        for i in range(9):
            if board[i][8-i] == 0:
                degree += 1
    return degree


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
    unassigned = select_unassigned_variable(board)
    if not unassigned:
        return True  # Sudoku solved

    row, col, options = unassigned
    
    for num in sorted(options):  # Sort to enforce the ORDER-DOMAIN-VALUES from low to high
        if is_consistent(board, row, col, num):
            board[row][col] = num
            if backtrack(board):
                return True
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
