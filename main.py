import pprint
import copy
from shapes_file import Shape, shapes


real_board = [[0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],]


def get_available_moves(board, shape):
    '''
    The function gets the current state of the board and the shape to be placed, returns all possible moves
    '''
    moves = []
    for shape_id, shape_obj in shapes.items():
        if shape_obj == shape:
            for row in range(len(board) - shape.height + 1):
                for col in range(len(board[0]) - shape.width + 1):
                    if is_valid_move(board, shape, row, col):
                        moves.append((shape_id, row, col))
    return moves

def apply_move_to_board(board, move, shape):
    '''
    Applies the selected move to the board
    '''
    shape_id, row, col = move
    shape_obj = shapes[shape_id]

    for r in range(shape_obj.height):
        for c in range(shape_obj.width):
            if shape_obj.grid[r][c] == 1:
                board[row + r][col + c] = 1
            # else:
            #     board[row + r][col + c] = 0
    new_b = check_and_remove_completed_regions(board)
    return new_b


def check_and_remove_completed_regions(board):
    '''
    removes the filled sections of the board
    '''
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            region_values = [board[i + x][j + y] for x in range(3) for y in range(3)]
            if all(value == 1 for value in region_values):
                for x in range(3):
                    for y in range(3):
                        board[i + x][j + y] = 'T'
    

    for i in range(9):
        if all(value == 1 or value == 'T' for value in board[i]):
            for j in range(9):
                board[i][j] = 'T'
    
    for j in range(9):
        column_values = [board[i][j] for i in range(9)]
        if all(value == 1 or value == 'T' for value in column_values):
            for i in range(9):
                board[i][j] = 'T'

    for i in range(0,9,1):
        for j in range(0,9,1):
            if board[i][j] == 'T':
                board[i][j] = 0
    return board



def is_valid_move(board, shape, row, col):
    '''
    Checks if a move is possible
    '''
    for r in range(shape.height):
        for c in range(shape.width):
            if shape.grid[r][c] == 1 and board[row + r][col + c] != 0:
                return False
    return True

def place_shape_on_board(board_1, move):
    '''
    Positions the piece on the field. There is the same function above, for convenience, I decided not to delete it
    '''
    shape_id, row, col = move
    shape = shapes[shape_id]
    for r in range(shape.height):
        for c in range(shape.width):
            if shape.grid[r][c] == 1:
                board_1[row + r][col + c] = 1

    apply_move_to_board(board_1, move, shape) ## EDITED
    
    

    return board_1


def evaluate_board(board):

    '''
    The main function is evaluating the board. You can change the algorithm to make it even better.
    '''
    score = 0
    
    # Проходим по каждой строке на доске
    for row in board:
        for pixel in row:
            if pixel == 1:
                score -= 1000
    '''
    За блок рядом с границей прибавлять не 1 очко, а 2
    '''
    for i in range(0, 9, 1):
        for j in range(0, 9, 1):
            # i;j
            if board[i][j] == 1:
                if i == 0 or i == 8:
                    score += 3  #3 - плохая идея
                if j == 0 or j == 8:
                    score += 3
                try:
                    if board[i + 1][j] == 1:
                        score += 1
                except IndexError:
                    pass

                try:
                    if board[i - 1][j] == 1:
                        score += 1

                except IndexError:
                    pass

                try:
                    if board[i][j + 1] == 1:
                        score += 1
                except IndexError:
                    pass

                try:
                    if board[i][j - 1] == 1:
                        score += 1
                except IndexError:
                    pass
    
    return score


    

def is_game_over(board, shape):
    '''
    Checks if any move is possible
    '''
    if get_available_moves(board, shape) == []:
        return True
    return False
    

def select_best_move(board, shape):
    '''
    Chooses the best move. It looks like a minimax algorithm
    '''
    b_1 = copy.deepcopy(board)

    best_move = None
    best_score = float('-inf')

    for move in get_available_moves(b_1, shape):

        temp_board = copy.deepcopy(b_1)
        temp_board = place_shape_on_board(temp_board, move)

        score = evaluate_board(temp_board)

        if score > best_score:
            best_score = score
            best_move = move
    return best_move


def visualize_move(board, move, shape):
    '''
    Displays where to go more explicitly
    '''
    visual_board = copy.deepcopy(board)
    shape_id, row, col = move
    shape_obj = shapes[shape_id]
    for r in range(shape_obj.height):
        for c in range(shape_obj.width):
            if shape_obj.grid[r][c] == 1:
                visual_board[row + r][col + c] = 'X'
            # else:
            #     visual_board[row + r][col + c] = '_'


    for row in visual_board:
        print(' '.join(map(str, row)))
    print()


def get_board(b_1):
    '''
    Displays the board in the console
    '''
    for row in b_1:
        print(' '.join(map(str, row)))
    print()



def start_game(board):
    '''
    Runs the algorithm
    '''
    shape = shapes[int(input('shape_id = '))]
    copy_board = copy.deepcopy(board)
    while not(is_game_over(copy_board, shape)):
        my_move = select_best_move(copy_board, shape)
        print("Best move:")
        #get_board(board)
        visualize_move(copy_board, my_move, shape)
        
        board = apply_move_to_board(board, my_move, shape)
       
        shape = shapes[int(input('shape_id = '))]
        copy_board = copy.deepcopy(board)
    print("Game over!")




if __name__ == '__main__':
     start_game(real_board)
        




# test_board = [[0,0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0,0],
#               [0,0,0,0,0,0,0,0,0],
#               [1,0,0,0,0,0,0,0,1],
#               [1,1,1,0,0,0,0,0,1],
#               [1,1,1,0,0,0,0,1,1]] 

# #-149950 #-59986
# print(len(get_available_moves(test_board, shape=shapes[407])))

# print()