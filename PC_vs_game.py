from shapes_file import shapes, Shape
import random
import copy
from main import is_game_over, select_best_move, apply_move_to_board, visualize_move, triple_moves


all_shapes = [shape for shape in shapes.values()]

real_board = [[0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],]

def pc_vs_pc(board):
    '''
    Runs the algorithm
    '''
    shape_1 = random.choice(all_shapes)
    shape_2 = random.choice(all_shapes)
    shape_3 = random.choice(all_shapes)
    my_shapes = [shape_1,shape_2,shape_3]
    copy_board = copy.deepcopy(board)
    counter = 0
    while (any(not is_game_over(copy_board, shape) for shape in my_shapes)):
        try:
            my_moves = triple_moves(copy_board, my_shapes)
        except:
            return counter
        #print("Best move:")
        #get_board(board)
        # for move in my_moves:
        #     visualize_move(copy_board, move[0], my_shapes)
        #     copy_board = apply_move_to_board(copy_board, move[0], move[0])
        
        #visualize_move(copy.deepcopy(board),my_moves[0][0], my_shapes)
        try:
            board = apply_move_to_board(board, my_moves[0][0])
            #visualize_move(copy.deepcopy(board),my_moves[1][0], my_shapes)
            board = apply_move_to_board(board, my_moves[1][0])
            #visualize_move(copy.deepcopy(board),my_moves[2][0], my_shapes)
            board = apply_move_to_board(board, my_moves[2][0])
        except:
            return counter
        counter += 3
        #print(counter)
        shape_1 = random.choice(all_shapes)
        shape_2 = random.choice(all_shapes)
        shape_3 = random.choice(all_shapes)
        my_shapes = [shape_1,shape_2,shape_3]
        copy_board = copy.deepcopy(board)
    #print("Game over!")
    return counter

if __name__ == '__main__':
    reses = []
    for i in range(200):
        real_board = [[0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0],]
        res = pc_vs_pc(real_board)
        reses.append(res*11)
        print(i)

print(reses)
print(sum(reses)/len(reses))
print(max(reses))




