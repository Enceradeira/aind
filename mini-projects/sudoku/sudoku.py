rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return



def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '.' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """

    grid_values = list(grid)

    possible_values = [x if x != '.' else cols for x in grid_values]

    return dict([(a,b) for a,b in zip(boxes,possible_values)])


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    result = dict(values)
    for box,value in values.items():
        if len(value) == 1:
            for peer in peers[box]:
                result[peer] = result[peer].replace(value,'')
    
    return result;


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    result = dict(values)
    for unit in unitlist:
        for digit in cols:
            box_with_digit = [box for box in unit if digit in values[box]]
            if len(box_with_digit) == 1:
                result[box_with_digit[0]] = digit
    return result

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    reduced_values = reduce_puzzle(values)
    if not reduced_values:
        return False
    
    # Choose one of the unfilled squares with the fewest possibilities
    length_of_unsovled = [len(value) for value in reduced_values.values() if len(value)>1]
    if len(length_of_unsovled) == 0:
        return reduced_values

    min_length_unsolved = min(length_of_unsovled)
    box, value = [(b,v) for b,v in reduced_values.items() if len(v) == min_length_unsolved][0]
        
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for possible_value in value:
        possible_solution = dict(reduced_values)
        possible_solution[box] = possible_value
        result = search(possible_solution)
        if result:
            return result

    return False
        
difficult_sudoku = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
easy_sudoku = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

possible_values = grid_values(difficult_sudoku)
display(possible_values)

print('\n\n')

#eliminated_values = eliminate(possible_values)
#display(eliminated_values)

#print('\n\n')

#for x in range(0,20):
#    eliminated_values = only_choice(eliminated_values)
#display(eliminated_values)

#reduced_values = reduce_puzzle(possible_values)
#display(reduced_values)

searched_values = search(possible_values)
display(searched_values)
