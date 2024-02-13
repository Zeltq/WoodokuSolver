from shapes_file import shapes, Shape
import random
import copy
from main import is_game_over, select_best_move, apply_move_to_board, visualize_move, get_board


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
    counter = 0
    shape = random.choice(all_shapes)
    copy_board = copy.deepcopy(board)
    while not(is_game_over(copy_board, shape)):
        my_move = select_best_move(copy_board, shape)
        #print("Best move:")
        #visualize_move(copy_board, my_move, shape)
        
        board = apply_move_to_board(board, my_move, shape)
       
        shape = random.choice(all_shapes)
        copy_board = copy.deepcopy(board)
        counter += 1
    #print("Game over!")
    return counter*8.9

if __name__ == '__main__':
    reses = []
    for i in range(100):
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
        reses.append(res)

print(sum(reses)/len(reses))




