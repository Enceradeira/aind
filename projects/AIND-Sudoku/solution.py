from functools import reduce
import pdb


# Helpers
assignments = []
def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

# Constants
rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
tuple_concat = lambda t: t[0]+t[1]
diagonal_units = [list(map(tuple_concat, zip(rows,cols))),list(map(tuple_concat, zip(rows,reversed(cols))))]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)



# Solution
def find_naked_twins(values):
    """Returns a tuple of boxes which share a unique set of values
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        a dictionary with twins and their common value and the units in which the pair occurrs 
        in of form {('F3','I3') : ('89',[['A3','B3','C3','D3','E3','F3','G3','H3','I3']])
    """

    result = {}
    for unit in unitlist:
        values_and_boxes = {}
        box_and_values_in_unit= [(box,values[box]) for box in unit if len(values[box]) == 2]
        for k,v in box_and_values_in_unit:
            if v in values_and_boxes:
                values_and_boxes[v].append(k)        
            else:
                values_and_boxes[v] = [k]
        for value, boxes in [(v,b) for v,b in values_and_boxes.items() if len(b) == 2]:
            twins = (boxes[0],boxes[1])
            if twins in result:
                result[twins][1].append(unit)
            else:
                result[twins] = (value,[unit])
        
    return result

def remove_values_from_peers(set_of_values, peers, values):
    """Removes a set of values from the values of the box's peers
    Args:
        peers: a list of all peers from whose the values are being removed (e.g. ['A1','B2','C3'])
        set_of_values: a set of values being removed from the peer's values (e.g '145' denoting value 1,4,5) 
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        a tuple in form (True,{'C3':'7','C4':'9', 'C5':'12'})
        the boolean indicates if any values could be removed from the values(dict)
        the values dictionary with the set of values removed from their peers
    """
    any_changes = False
    for peer in peers:
        for value in set_of_values:
            peer_values = values[peer]
            if len(peer_values) > 1:
                new_value = peer_values.replace(value,'')
                assign_value(values, peer, new_value)
                any_changes = any_changes or peer_values != new_value

    return (any_changes, values)

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    while True:
        any_changes = False

        # Find all instances of naked twins
        all_twins_and_values = find_naked_twins(values)

        # Eliminate the naked twins as possibilities for their peers
        for twins,info in all_twins_and_values.items(): 
            values_to_remove = info[0]
            units = info[1]
        
            for unit in units:
                peers_without_twins = [p for p in unit if p not in twins]
                has_unit_changed, values = remove_values_from_peers(values_to_remove, peers_without_twins, values)
                any_changes = any_changes or has_unit_changed
    
        if not any_changes:
            return values
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    grid_values = list(grid)

    possible_values = [x if x != '.' else cols for x in grid_values]

    return dict([(a,b) for a,b in zip(boxes,possible_values)])

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

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    for box,value in values.items():
        if len(value) == 1:
            for peer in peers[box]:
                assign_value(values, peer, values[peer].replace(value,''))
    
    return values;

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for digit in cols:
            box_with_digit = [box for box in unit if digit in values[box]]
            if len(box_with_digit) == 1:
                assign_value(values, box_with_digit[0], digit )
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        
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
        values = search(possible_solution)
        if values:
            return values

    return False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
