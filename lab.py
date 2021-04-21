#!/usr/bin/env python3
"""6.009 Lab -- Six Double-Oh Mines"""

# NO IMPORTS ALLOWED!

def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f'{key}:')
            for inner in val:
                print(f'    {inner}')
        else:
            print(f'{key}:', val)


# 2-D IMPLEMENTATION

# used in original 2d refactoring
# def is_in_board(board, r, c):
#     """
#     Parameters:
#         board: game board
#         r: location's row
#         c: location's column
#     Returns:
#         True if location (r, c) is in the board, False if it isn't
#     """
#     return r >= 0 and r < len(board) and c >= 0 and c < len(board[0])

# used in original 2d refactoring
# def get_num_bombs_around(board, r, c):
#     """
#     Parameters:
#         board: game board
#         r: location's row
#         c: location's column
#     Returns:
#         number of neighboring bombs (refactored from original into a shorter helper function)
#     """
#     neighbor_bombs = 0
#     # used a set to hold the 9 locations to check for bombs
#     neighbors = {(r-1, c-1), (r-1, c), (r-1, c+1), (r, c-1), (r, c), (r, c+1), (r+1, c-1), (r+1, c), (r+1, c+1)}
#     # for each location, if it is in the board and a bomb, increment the number of neighbor bombs
#     for n in neighbors:
#         if is_in_board(board, n[0], n[1]) and board[n[0]][n[1]] == '.':
#             neighbor_bombs += 1
#     return neighbor_bombs

def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'mask' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    coords: {(0, 1), (1, 2), (0, 0), (1, 1), (0, 3), (0, 2), (1, 0), (1, 3)}
    dimensions: (2, 4)
    mask:
        [False, False, False, False]
        [False, False, False, False]
    state: ongoing
    """
    return new_game_nd((num_rows, num_cols), bombs)
    # used in original 2d refactoring
    # refactored setting up board using list comprehensions
    # board = [[0 for _ in range(num_cols)] for _ in range(num_rows)]
    # # since bombs are in a list, I didn't want to do contains checks repeatedly
    # # instead, after board is initialized with all 0s, loop over bombs once
    # for bomb in bombs:
    #     board[bomb[0]][bomb[1]] = '.'

    # # refactored setting up mask using list comprehensions to intialize it to dimensions of board with all values being False
    # mask = [[False for _ in range(num_cols)] for _ in range(num_rows)]

    # # refactored neighboring bombs, added helper function to handle getting number of bombs surrounding
    # for r in range(num_rows):
    #     for c in range(num_cols):
    #         if board[r][c] == 0: # if location is not a bomb, set value equal to how many bombs are surrounding it
    #             board[r][c] = get_num_bombs_around(board, r, c)
    
    # return { 'dimensions': (num_rows, num_cols), 'board' : board, 'mask' : mask, 'state': 'ongoing'}


# used in original 2d refactoring
# def is_board_cleared(board, mask):
#     """
#     Parameters:
#         board: game board
#     Returns:
#         True if all safe squares have been revealed
#     """
#     for r in range(len(board)):
#         for c in range(len(board[0])):
#             if board[r][c] != '.' and mask[r][c] == False:
#                 return False
#     return True

def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['mask'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is visible on the board after digging (i.e. game['mask'][bomb_location] ==
    True), 'victory' when all safe squares (squares that do not contain a bomb)
    and no bombs are visible, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'coords': {(0, 1), (1, 2), (0, 0), (1, 1), (0, 3), (0, 2), (1, 0), (1, 3)},
    ...         'mask': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    coords: {(0, 1), (1, 2), (0, 0), (1, 1), (0, 3), (0, 2), (1, 0), (1, 3)}
    dimensions: (2, 4)
    mask:
        [False, True, True, True]
        [False, False, True, True]
    state: victory

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'coords': {(0, 1), (1, 2), (0, 0), (1, 1), (0, 3), (0, 2), (1, 0), (1, 3)},
    ...         'mask': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    coords: {(0, 1), (1, 2), (0, 0), (1, 1), (0, 3), (0, 2), (1, 0), (1, 3)}
    dimensions: [2, 4]
    mask:
        [True, True, False, False]
        [False, False, False, False]
    state: defeat
    """
    return dig_nd(game, (row, col))
    # used in original 2d refactoring
    # player already won/lost or dug up this spot
    # if game['state'] == 'defeat' or game['state'] == 'victory' or game['mask'][row][col] == True:
    #     return 0
    # game['mask'][row][col] = True

    # # player revealed a bomb
    # if game['board'][row][col] == '.':
    #     game['state'] = 'defeat'
    #     return 1

    # # removed unneccesary and duplicate code to make function shorter and easier to understand
    # # EXAMPLES
    #     # checking for the number of bombs revealed was not necessary since after one bomb 
    #     # is revealed the game state is changed to defeat, and the functions always returns 0

    #     # added a helper function to check if all safe squares had been revealed, instead of looping
    #     # over entire board and calculating how many safe squares were covered since only needed to
    #     # know if there was at least 1 safe square covered to say that player hadn't won

    # # if location has no adjacent bombs then recursively reveal (dig up) its eight neighbors
    # revealed = 1
    # if game['board'][row][col] == 0:
    #     neighbors = {(row-1, col-1), (row-1, col), (row-1, col+1), (row, col-1), (row, col), (row, col+1), (row+1, col-1), (row+1, col), (row+1, col+1)}
    #     # for each location, if it is in the board and not a bomb and hasn't been revealed already, dig it up
    #     for n in neighbors:
    #         if is_in_board(game['board'], n[0], n[1]) and game['board'][n[0]][n[1]] != '.':
    #             if game['mask'][n[0]][n[1]] == False:
    #                 revealed += dig_2d(game, n[0], n[1])

    # # player revealed all non-bomb squares, so they won!
    # if is_board_cleared(game['board'], game['mask']):
    #     game['state'] = 'victory'

    # return revealed


def render_2d(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring bombs).
    game['mask'] indicates which squares should be visible.  If xray is True (the
    default is False), game['mask'] is ignored and all cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['mask']

    Returns:
       A 2D array (list of lists)

    >>> render_2d({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'coords': {(0, 1), (1, 2), (0, 0), (1, 1), (0, 3), (0, 2), (1, 0), (1, 3)},
    ...         'mask':  [[False, True, True, False],
    ...                   [False, False, True, False]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'coords': {(0, 1), (1, 2), (0, 0), (1, 1), (0, 3), (0, 2), (1, 0), (1, 3)},
    ...         'mask':  [[False, True, False, True],
    ...                   [False, False, False, True]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    return render_nd(game, xray)
    # used in original 2d refactoring
    # board_array = []
    # for row in range(game['dimensions'][0]):
    #     new_row = []
    #     for col in range(game['dimensions'][1]):
    #         if xray or game['mask'][row][col]:
    #             if game['board'][row][col] == 0:
    #                 new_row.append(' ')
    #             else:
    #                 new_row.append(str(game['board'][row][col]))
    #         else:
    #             new_row.append('_')   
    #     board_array.append(new_row)
    # return board_array


def render_ascii(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function 'render_2d(game)'.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['mask']

    Returns:
       A string-based representation of game

    >>> print(render_ascii({'dimensions': (2, 4),
    ...                     'state': 'ongoing',
    ...                     'board': [['.', 3, 1, 0],
    ...                               ['.', '.', 1, 0]],
    ...                     'mask':  [[True, True, True, False],
    ...                               [False, False, True, False]]}))
    .31_
    __1_
    """
    ascii_board = ""
    for row in range(game['dimensions'][0]):
        if ascii_board:   
            ascii_board += "\n"
        for col in range(game['dimensions'][1]):
            if xray or game['mask'][row][col]:
                if game['board'][row][col] == 0:
                    ascii_board += " "  
                else:
                    ascii_board += str(game['board'][row][col])
            else:
                ascii_board += "_"
    return ascii_board




# N-D IMPLEMENTATION

def get_nd_value(board, coord):
    """
    Parameters:
        nd: n-dimensional array
        coord: tuple of coordinates
    Returns:
        value at those coordinates in the array
    >>> game = new_game_nd((2, 4, 3), [(0, 0, 1), (1, 3, 2), (0, 1, 2)])
    >>> get_nd_value(game['board'], (1, 2, 1))
    2
    >>> get_nd_value(game['board'], (0, 0, 1))
    '.'
    """
    value = board
    for c in coord:
        value = value[c]
    return value

def set_nd_value(board, coord, val):
    """
    Replaces the value at those coordinates in the array with the given value
    Parameters:
        nd: n-dimensional array
        coord: tuple of coordinates
        val: value to replace with
    """
    value = board
    for idx, c in enumerate(coord):
        if idx == len(coord) - 1:
            value[coord[-1]] = val
        else:
            value = value[c]

def get_nd_copy(board):
    """
    Parameters:
        board: game board
    Returns:
        a copy of the n-dimensional game board
    >>> game = new_game_nd((2, 4, 3), [(0, 0, 1), (1, 3, 2), (0, 1, 2)])
    >>> g = get_nd_copy(game['board'])
    >>> set_nd_value(g, (1, 0, 2), 10)
    >>> print(g)
    [[[1, '.', 2], [1, 2, '.'], [0, 2, 2], [0, 1, 1]], [[1, 2, 10], [1, 2, 2], [0, 2, 2], [0, 1, '.']]]
    """
    if not board:
        return []
    if isinstance(board[0], list):
        return [get_nd_copy(board[0])[:]] + get_nd_copy(board[1:])
    return board

def create_nd(dim, val):
    """
    Creates a new N-d array with given dimensions where each value in the array is the given value
    Parameters:
        dim: dimensions of n-dimensional array to create
        val: value to use everywhere in the array
    >>> create_nd((2, 4, 3), 0)
    [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]
    """
    nd = [val for _ in range(dim[-1])]
    for d in reversed(dim[:-1]):
        nd = [get_nd_copy(nd)[:] for _ in range(d)]
    return nd

def get_nd_coordinates(dim, coords=None):
    """
    Parameters:
        dim: dimensions game board
    Returns all possible coordinates of board
    >>> get_nd_coordinates((2, 4, 3))
    {(0, 1, 0), (0, 3, 0), (1, 2, 2), (1, 3, 0), (0, 0, 1), (0, 2, 1), (1, 0, 1), (1, 1, 0), (0, 1, 2), (0, 3, 2), (1, 2, 1), (1, 3, 2), (0, 2, 0), (0, 0, 0), (1, 1, 2), (1, 0, 0), (0, 1, 1), (0, 3, 1), (1, 2, 0), (1, 3, 1), (0, 0, 2), (0, 2, 2), (1, 0, 2), (1, 1, 1)}
    """
    if not dim: # base case, no dimensions left
        return set()
    if not coords:
        coords = set()
        for d in range(dim[0]):
            coords.add((d,))
    else:
        prev_coords = coords.copy()
        coords.clear()
        for d in range(dim[0]):
            for c in prev_coords:
                coords.add(c + (d,))
    return coords | get_nd_coordinates(dim[1:], coords)
    
def get_nd_neighbors(dim, coord, idx=0, neighbors=None):
    """
    Parameters:
        board: game board
        coord: tuple location to get neighbors of
    Returns the coordinates of all the neighbors of coord
    >>> get_nd_neighbors((2, 4, 3), (1, 0, 1))
    {(0, 1, 0), (0, 0, 0), (1, 1, 2), (1, 0, 0), (0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 0), (0, 0, 2), (0, 1, 2), (1, 0, 2), (1, 1, 1)}
    """
    if idx == len(dim): # base case, no dim left
        return set()
    if not neighbors:
        neighbors = { coord }
    cur_neigbhors = neighbors.copy()
    for c in cur_neigbhors:
        if coord[idx]+1 < dim[idx]:
            neighbors.add(c[:idx] + (coord[idx]+1,) + c[idx+1:])
        if coord[idx]-1 >= 0:
            neighbors.add(c[:idx] + (coord[idx]-1,) + c[idx+1:])
    return neighbors | get_nd_neighbors(dim, coord, idx+1, neighbors)

def get_nd_covered_squares(game):
    """
    Parameters:
        board: game board
    Returns:
        number of safe squares that are covered
    >>> game = new_game_nd((2, 4, 3), [(0, 0, 1), (1, 3, 2), (0, 1, 2)])
    >>> get_nd_covered_squares(game)
    21
    >>> dig_nd(game, (1, 2, 0))
    12
    >>> get_nd_covered_squares(game)
    9
    """
    covered_squares = 0
    for c in game['coords']:
        if get_nd_value(game['board'], c) != '.' and get_nd_value(game['mask'], c) == False:
            covered_squares += 1
    return covered_squares

def new_game_nd(dimensions, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'mask' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of lists, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    coords: {(1, 2, 1), (0, 1, 0), (0, 2, 0), (0, 0, 0), (0, 3, 0), (1, 0, 0), 
    (1, 3, 0), (0, 0, 1), (0, 1, 1), (0, 2, 1), (1, 0, 1), (1, 1, 0), (0, 3, 1), 
    (1, 2, 0), (1, 3, 1), (1, 1, 1)}
    dimensions: (2, 4, 2)
    mask:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    state: ongoing
    >>> game = new_game_nd((3,3,2),[(1,2,0)])
    >>> dump(game)
    board:
        [[0, 0], [1, 1], [1, 1]]
        [[0, 0], [1, 1], ['.', 1]]
        [[0, 0], [1, 1], [1, 1]]
    coords: {(1, 2, 1), (0, 1, 0), (2, 1, 0), (0, 2, 0), (0, 0, 0), (1, 0, 0), 
    (2, 0, 0), (0, 0, 1), (2, 2, 0), (0, 1, 1), (2, 1, 1), (0, 2, 1), (1, 0, 1), 
    (1, 1, 0), (1, 2, 0), (2, 0, 1), (2, 2, 1), (1, 1, 1)}
    dimensions: (3, 3, 2)
    mask:
        [[False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False]]
    state: ongoing
    """
    board = create_nd(dimensions, 0)
    for bomb in bombs:
        set_nd_value(board, bomb, '.')
    mask = create_nd(dimensions, False)

    coords = get_nd_coordinates(dimensions)
    for c in coords:
        # if location is not a bomb, set value equal to how many bombs are surrounding it
        if get_nd_value(board, c) == 0:
            num_bombs_around = 0
            for n in get_nd_neighbors(dimensions, c, 0):
                if get_nd_value(board, n) == '.':
                    num_bombs_around += 1
            set_nd_value(board, c, num_bombs_around)
    
    return { 'dimensions': dimensions, 'board' : board, 'mask' : mask, 'state': 'ongoing', 'coords': coords}


def dig_nd(game, coordinates, covered_squares=None, revealed=None):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the mask to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is visible on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are visible, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [False, False], [False, False]],
    ...               [[False, False], [False, False], [False, False], [False, False]]],
    ...      'state': 'ongoing',
    ...      'coords': {(1, 2, 1), (0, 1, 0), (0, 2, 0), (0, 0, 0), (0, 3, 0), (1, 0, 0), 
    ...      (1, 3, 0), (0, 0, 1), (0, 1, 1), (0, 2, 1), (1, 0, 1), (1, 1, 0), (0, 3, 1), 
    ...      (1, 2, 0), (1, 3, 1), (1, 1, 1)}}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    coords: {(1, 2, 1), (0, 1, 0), (0, 2, 0), (0, 0, 0), (0, 3, 0), (1, 0, 0), (1, 3, 0),
    (0, 0, 1), (0, 1, 1), (0, 2, 1), (1, 0, 1), (1, 1, 0), (0, 3, 1), (1, 2, 0), (1, 3, 1),
    (1, 1, 1)}
    dimensions: (2, 4, 2)
    mask:
        [[False, False], [False, True], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    state: ongoing
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [False, False], [False, False]],
    ...               [[False, False], [False, False], [False, False], [False, False]]],
    ...      'state': 'ongoing',
    ...      'coords': {(1, 2, 1), (0, 1, 0), (0, 2, 0), (0, 0, 0), (0, 3, 0), (1, 0, 0), 
    ...      (1, 3, 0), (0, 0, 1), (0, 1, 1), (0, 2, 1), (1, 0, 1), (1, 1, 0), (0, 3, 1), 
    ...      (1, 2, 0), (1, 3, 1), (1, 1, 1)}}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    coords: {(1, 2, 1), (0, 1, 0), (0, 2, 0), (0, 0, 0), (0, 3, 0), (1, 0, 0), 
    (1, 3, 0), (0, 0, 1), (0, 1, 1), (0, 2, 1), (1, 0, 1), (1, 1, 0), (0, 3, 1), 
    (1, 2, 0), (1, 3, 1), (1, 1, 1)}
    dimensions: (2, 4, 2)
    mask:
        [[False, True], [False, True], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    state: defeat
    """

    # player already won/lost or dug up this spot
    if game['state'] == 'defeat' or game['state'] == 'victory' or get_nd_value(game['mask'], coordinates) == True:
        return 0
    set_nd_value(game['mask'], coordinates, True)

    # player revealed a bomb
    value_at_coord = get_nd_value(game['board'], coordinates)
    if value_at_coord  == '.':
        game['state'] = 'defeat'
        return 1
    
    if not covered_squares:
        covered_squares = get_nd_covered_squares(game)
    if not revealed:
        revealed = 0
    revealed += 1

    # if location has no adjacent bombs then recursively reveal (dig up) its neighbors
    if value_at_coord == 0:
        # recursively dig up its neighbors
        for n in get_nd_neighbors(game['dimensions'], coordinates):
            # for each location, if it is not a bomb and hasn't been revealed already, dig it up
            if get_nd_value(game['board'], n) != '.' and get_nd_value(game['mask'], n) == False:
                revealed += dig_nd(game, n, covered_squares)

    # player revealed all non-bomb squares, so they won!
    if covered_squares < revealed:
        game['state'] = 'victory'

    return revealed

def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares
    neighboring bombs).  The mask indicates which squares should be
    visible.  If xray is True (the default is False), the mask is ignored
    and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    the mask

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [True, True], [True, True]],
    ...               [[False, False], [False, False], [True, True], [True, True]]],
    ...      'state': 'ongoing',
    ...      'coords': {(1, 2, 1), (0, 1, 0), (0, 2, 0), (0, 0, 0), (0, 3, 0), (1, 0, 0), 
    ...      (1, 3, 0), (0, 0, 1), (0, 1, 1), (0, 2, 1), (1, 0, 1), (1, 1, 0), (0, 3, 1), 
    ...      (1, 2, 0), (1, 3, 1), (1, 1, 1)} }
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]
    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    render = get_nd_copy(game['board'])
    for c in game['coords']:
        if xray or get_nd_value(game['mask'], c):
            val = get_nd_value(game['board'], c)
            if val == 0:
                set_nd_value(render, c, ' ')
            else:
                set_nd_value(render, c, str(val))
        else:
            set_nd_value(render, c, '_')
    return render
            


if __name__ == "__main__":

    # Test with doctests. Helpful to debug individual lab.py functions.
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags) #runs ALL doctests
    
    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d or any other function you might want.  To do so, comment
    # out the above line, and uncomment the below line of code. This may be
    # useful as you write/debug individual doctests or functions.  Also, the
    # verbose flag can be set to True to see all test results, including those
    # that pass.
    #
    # doctest.run_docstring_examples(dig_2d, globals(), optionflags=_doctest_flags, verbose=False)
