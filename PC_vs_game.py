from shapes_file import shapes, Shape
import random
import copy
from main import apply_move_to_board, visualize_move, good_alg, get_board


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
    
    shape_1 = random.choice(all_shapes)
    shape_2 = random.choice(all_shapes)
    shape_3 = random.choice(all_shapes)
    my_shapes = [shape_1,shape_2,shape_3]
    copy_board = copy.deepcopy(board)
    counter = 0
    while True:
        print(f'Score +- : {counter*10}')
        
        try:
            moves = good_alg(copy_board, my_shapes)
        except:
            return counter
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
        counter += 3
        print(f'board:')
        get_board(board)
        shape_1 = random.choice(all_shapes)
        shape_2 = random.choice(all_shapes)
        shape_3 = random.choice(all_shapes)
        my_shapes = [shape_1,shape_2,shape_3]
        copy_board = copy.deepcopy(board)

    

if __name__ == '__main__':
    reses = []
    for i in range(1):
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
        reses.append(res*10)
        print(i)

print(reses)
print(sum(reses)/len(reses))
print(max(reses))




