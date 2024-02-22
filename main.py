import pprint
import copy
from shapes_file import Shape, shapes
from itertools import permutations


real_board = [[1,1,0,0,0,0,0,0,0],
              [1,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0],
              [1,0,0,1,0,0,0,0,0],
              [0,0,0,0,0,0,0,1,1],
              [1,0,0,0,0,0,1,1,0],
              [0,0,0,1,1,1,1,0,0],
              [0,0,0,1,1,0,1,0,0],
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

def apply_move_to_board(board, move):
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

    apply_move_to_board(board_1, move) ## EDITED
    
    

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
    # for i in range(0, 9, 1):
    #     for j in range(0, 9, 1):
    #         # i;j
    #         if board[i][j] == 1:
    #             if i == 0 or i == 8:
    #                 score += 1  #3 - плохая идея
    #             if j == 0 or j == 8:
    #                 score += 1
    #             try:
    #                 if board[i + 1][j] == 1:
    #                     score += 1
    #             except IndexError:
    #                 pass

    #             try:
    #                 if board[i - 1][j] == 1:
    #                     score += 1

    #             except IndexError:
    #                 pass

    #             try:
    #                 if board[i][j + 1] == 1:
    #                     score += 1
    #             except IndexError:
    #                 pass

    #             try:
    #                 if board[i][j - 1] == 1:
    #                     score += 1
    #             except IndexError:
    #                 pass
    for i in range(0,8,1):
        for j in range(0, 8, 1):
            if board[i][j] == 1 and board[i + 1][j] == 1 and board[i][j + 1] == 1:
                score += 1

    for i in range(1,8,1):
        for j in range(1, 8, 1):
            if board[i][j] == 0 and board[i + 1][j] == 1 and board[i][j + 1] == 1 and board[i-1][j] == 1 and board[i][j-1] == 1:
                score -=1

    # for row in board:
    #     if sum(row) == 8 and row[0] == 1 and row[8] == 1:
    #         score += 50

    # for i in range(9):
    #     if sum(row[i] for row in board) == 8 and board[0][i] == 1 and board[8][i] == 1:
    #         score += 50

    
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

    return [best_score, best_move, shape]

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

def triple_moves(board, shapes):
    score_1 = select_best_move(copy.deepcopy(board), shapes[0])[0]
    move_1 = select_best_move(copy.deepcopy(board), shapes[0])[1:]
    score_2 = select_best_move(copy.deepcopy(board), shapes[1])[0]
    move_2 = select_best_move(copy.deepcopy(board), shapes[1])[1:]
    score_3 = select_best_move(copy.deepcopy(board), shapes[2])[0]
    move_3 = select_best_move(copy.deepcopy(board), shapes[2])[1:]
    #print(move_3)

    if score_1 > score_2 and score_1 > score_3: #Первый ход самый выгодный
        first_move = move_1
        board = apply_move_to_board(board, move_1[0])

        score_2_2 = select_best_move(copy.deepcopy(board), shapes[1])[0]
        move_2_2 = select_best_move(copy.deepcopy(board), shapes[1])[1:]
        score_3_2 = select_best_move(copy.deepcopy(board), shapes[2])[0]
        move_3_2 = select_best_move(copy.deepcopy(board), shapes[2])[1:]
        if score_2_2 > score_3_2:
            second_move = move_2_2
            board = apply_move_to_board(board, move_2_2[0])
            third_move = select_best_move(copy.deepcopy(board), shapes[2])[1:]

        else:
            second_move = move_3_2
            board = apply_move_to_board(board, move_3_2[0])
            third_move = select_best_move(copy.deepcopy(board), shapes[1])[1:]
            
    elif score_2 > score_1 and score_2 > score_3: #Второй ход самый выгодный
        first_move = move_2
        board = apply_move_to_board(board, move_2[0])

        score_1_2 = select_best_move(copy.deepcopy(board), shapes[0])[0]
        move_1_2 = select_best_move(copy.deepcopy(board), shapes[0])[1:]
        score_3_2 = select_best_move(copy.deepcopy(board), shapes[2])[0]
        move_3_2 = select_best_move(copy.deepcopy(board), shapes[2])[1:]
        if score_1_2 > score_3_2:
            second_move = move_1_2
            board = apply_move_to_board(board, move_1_2[0])
            third_move = select_best_move(copy.deepcopy(board), shapes[2])[1:]

        else:
            second_move = move_3_2
            board = apply_move_to_board(board, move_3_2[0])
            third_move = select_best_move(copy.deepcopy(board), shapes[0])[1:]

    else: #Третий ход самый выгодный

        first_move = move_3
        board = apply_move_to_board(board, move_3[0])

        score_1_2 = select_best_move(copy.deepcopy(board), shapes[0])[0]
        move_1_2 = select_best_move(copy.deepcopy(board), shapes[0])[1:]
        score_2_2 = select_best_move(copy.deepcopy(board), shapes[1])[0]
        move_2_2 = select_best_move(copy.deepcopy(board), shapes[1])[1:]
        if score_1_2 > score_2_2:
            second_move = move_1_2
            board = apply_move_to_board(board, move_1_2[0])
            third_move = select_best_move(copy.deepcopy(board), shapes[1])[1:]
        else:
            second_move = move_2_2
            board = apply_move_to_board(board, move_2_2[0])
            third_move = select_best_move(copy.deepcopy(board), shapes[0])[1:]
            
    #print(first_move, second_move, third_move)
    return [first_move, second_move, third_move]

def start_game(board):
    '''
    Runs the algorithm
    '''
    shape_1 = shapes[int(input('shape_id = '))]
    shape_2 = shapes[int(input('shape_id = '))]
    shape_3 = shapes[int(input('shape_id = '))]
    my_shapes = [shape_1,shape_2,shape_3]
    copy_board = copy.deepcopy(board)
    while (any(not is_game_over(copy_board, shape) for shape in my_shapes)):

        my_moves = triple_moves(copy_board, my_shapes)
        print("Best move:")
        #get_board(board)
        # for move in my_moves:
        #     visualize_move(copy_board, move[0], my_shapes)
        #     copy_board = apply_move_to_board(copy_board, move[0], move[0])
        
        visualize_move(copy.deepcopy(board),my_moves[0][0], my_shapes)
        board = apply_move_to_board(board, my_moves[0][0])
        visualize_move(copy.deepcopy(board),my_moves[1][0], my_shapes)
        board = apply_move_to_board(board, my_moves[1][0])
        visualize_move(copy.deepcopy(board),my_moves[2][0], my_shapes)
        board = apply_move_to_board(board, my_moves[2][0])
       
        shape_1 = shapes[int(input('shape_id = '))]
        shape_2 = shapes[int(input('shape_id = '))]
        shape_3 = shapes[int(input('shape_id = '))]
        my_shapes = [shape_1,shape_2,shape_3]
        copy_board = copy.deepcopy(board)
    print("Game over!")

def start_game_2(board):
    
    shape_1 = shapes[int(input('shape_id = '))]
    shape_2 = shapes[int(input('shape_id = '))]
    shape_3 = shapes[int(input('shape_id = '))]
    my_shapes = [shape_1,shape_2,shape_3]
    copy_board = copy.deepcopy(board)
    while True:
        moves = good_alg(copy_board, my_shapes)
        
        print("Best moveS:")
        print('Move 1:')
        visualize_move(copy.deepcopy(board), moves[0], my_shapes)
        board = apply_move_to_board(board, moves[0])
        print('Move 2:')
        visualize_move(copy.deepcopy(board), moves[1], my_shapes)
        board = apply_move_to_board(board, moves[1])
        print('Move 3:')
        visualize_move(copy.deepcopy(board), moves[2], my_shapes)
        board = apply_move_to_board(board, moves[2])
        
        shape_1 = shapes[int(input('shape_id = '))]
        shape_2 = shapes[int(input('shape_id = '))]
        shape_3 = shapes[int(input('shape_id = '))]
        my_shapes = [shape_1,shape_2,shape_3]
        copy_board = copy.deepcopy(board)

def triple_moves_in_order(board, order):
    boards_after_move_1 = []
    real_moves = []

    for move in get_available_moves(board, order[0]):
        boards_after_move_1.append([apply_move_to_board(copy.deepcopy(board), move), move])

    boards_after_move_2 = []

    for b in boards_after_move_1:
        for move in get_available_moves(b[0], order[1]):
            boards_after_move_2.append([apply_move_to_board(copy.deepcopy(b[0]), move), [b[1], move]])


    max_score = float('-inf')
    for b in boards_after_move_2:
        for move in get_available_moves(b[0], order[2]):
            new_b = apply_move_to_board(copy.deepcopy(b[0]), move)
            score = evaluate_board(new_b)
            if score > max_score:
                max_score = score
                real_moves = b[1] + [move]
            #boards_after_move_3.append([new_b, b[1] + [move]])
    

    return [real_moves, max_score]

# print(triple_moves_in_order(real_board, [shapes[504],shapes[504],shapes[504]]))
# print(triple_moves_in_order(real_board, [shapes[504],shapes[504],shapes[504]]))
# print(triple_moves_in_order(real_board, [shapes[504],shapes[504],shapes[504]]))
# print(triple_moves_in_order(real_board, [shapes[504],shapes[504],shapes[504]]))
# print(triple_moves_in_order(real_board, [shapes[504],shapes[504],shapes[504]]))
# print(triple_moves_in_order(real_board, [shapes[504],shapes[504],shapes[504]]))






def good_alg(board,shapes):
    max_score = float('-inf')
    ords_1 = [shapes[0], shapes[1],shapes[2]]
    ords_2 = [shapes[0], shapes[2],shapes[1]] 
    ords_3 = [shapes[1], shapes[2],shapes[0]]
    ords_4 = [shapes[1], shapes[0],shapes[2]]
    ords_5 = [shapes[2], shapes[0],shapes[1]]
    ords_6 = [shapes[2], shapes[1],shapes[0]]
    possible_orders = [ords_1,ords_2,ords_3,ords_4,ords_5,ords_6]
    for order in possible_orders:
        copy_board = copy.deepcopy(board)
        result = triple_moves_in_order(copy_board, order)
        if result[1] > max_score:
            moves = result[0]
            max_score = result[1]
    return moves
        











if __name__ == '__main__':
    start_game_2(real_board)
    #print(good_alg(real_board, [shapes[504],shapes[504],shapes[504]]))
        



