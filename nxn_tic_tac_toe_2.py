#########################
#
# n x n Tic Tac Toe Minimax
# Author: Max Dickman
#
# Program to play n x n or
# n x n x n Tic Tac Toe
# using minimax with alpha
# beta pruning and memoization
# Utilizes separate board class
# for memoization
#
#########################

# TODO: FIX 3D STUFF

import board as b
import random
from functools import lru_cache

def clear():
    for i in range(40):
        print()

@lru_cache(maxsize=50000)
def minimax_2d(board, depth, alpha, beta, maximizing_player):
    '''
    Minimax algorithm using the static_eval function defined below

    Notes:
    X is the maximizing player
    '''
    
    empty_spaces = []
    winner = False

    if depth > 3:
        winner = board.check_win_2d()
        
    max_depth = int(5 / (board.n - 2)) + 5

    if depth == 0:
        print('Thinking...')

    for i in range(len(board.linear_board)):
        if board.linear_board[i] == ' ':
            empty_spaces.append(i)
    
    if winner or len(empty_spaces) == 0 or depth >= max_depth:
        return board.static_eval(depth, winner), 0

    if maximizing_player:
        max_eval = -1000000
        evals = {}

        # Loop through next possible moves to determine order
        for space in empty_spaces:
            evals.update(board.heuristic_eval(space, 'X'))

        order = sorted(evals, key=evals.get, reverse=True)

        # Loop through next possible moves in order
        for space in order:            
            board.move(space, 'X')
            evaluation = minimax_2d(board, depth + 1, alpha, beta, False)[0]
            board.move(space, ' ')
            max_eval = max(max_eval, evaluation)

            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        
        return max_eval, space
    else:
        min_eval = 1000000
        evals = {}

        # Loop through next possible moves to determine order
        for space in empty_spaces:
            evals.update(board.heuristic_eval(space, 'O'))

        order = sorted(evals, key=evals.get)

        # Loop through next possible moves in order
        for space in order:
            board.move(space, 'O')
            evaluation = minimax_2d(board, depth + 1, alpha, beta, True)[0]
            board.move(space, ' ')
            
            if evaluation < min_eval:
                min_eval = evaluation
                best_index = space

            beta = min(beta, evaluation)
            if beta <= alpha:
                break

            if depth == 0:
                print(str(space + 1) + ': ' + str(evaluation))
        
        if depth == 0:
            print(minimax_2d.cache_info())
        
        return min_eval, best_index

@lru_cache(maxsize=100000)
def minimax_3d(board, depth, alpha, beta, maximizing_player):
    # TODO: OPTIMIZE AND MAKE THIS RUN FASTER
    empty_spaces = []
    winner = False

    if depth > 3:
        winner = board.check_win_3d()
        
    max_depth = int(6 / (board.n - 1)) + 4

    if depth == 0:
        print('Thinking...')

    for i in range(len(board.linear_board)):
        if board.linear_board[i] == ' ':
            empty_spaces.append(i)

    if len(empty_spaces) == 0 or winner or depth >= max_depth: # figure out last condition
        return board.static_eval(depth, winner), 0

    if maximizing_player:
        max_eval = -1000000
        evals = {}
        
        for space in empty_spaces:
            evals.update(board.heuristic_eval(space, 'X'))

        order = sorted(evals, key=evals.get, reverse=True)

        # Loop through next possible moves
        for space in order:
            board.move(space, 'X')
            evaluation = minimax_3d(board, depth + 1, alpha, beta, False)[0]
            board.move(space, ' ')
            max_eval = max(max_eval, evaluation)

            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
            
        return max_eval, space
    else:
        min_eval = 1000000
        evals = {}
        
        for space in empty_spaces:
            evals.update(board.heuristic_eval(space, 'O'))

        order = sorted(evals, key=evals.get)
        
        # Loop through next possible moves
        for space in order:
            board.move(space, 'O')
            evaluation = minimax_3d(board, depth + 1, alpha, beta, True)[0]
            board.move(space, ' ')
            
            if evaluation < min_eval:
                min_eval = evaluation
                best_index = space

            beta = min(beta, evaluation)
            if beta <= alpha:
                break

            if depth == 0:
                print(str(space + 1) + ': ' + str(evaluation))

        if depth == 0:
            print(minimax_3d.cache_info())
        
        return min_eval, best_index

def player_o(board, moves):
    # TODO: ADD 3D MINIMAX

    max_index = board.n - 1
    
    if board.dimensions == 2:
        k = 0
        win, loc = board.almost_win_2d()

        if win:
            for i in range(board.n):
                if (win == 'dia' and loc == 0
                    and board.board[i][i] == ' '):
                    return board.convert_coords(i, i)
                elif (win == 'dia' and loc == 1
                      and board.board[i][max_index - i] == ' '):
                    return board.convert_coords(i, max_index - i)
                elif win == 'row' and board.board[loc][i] == ' ':
                    return board.convert_coords(loc, i)
                elif win == 'col' and board.board[i][loc] == ' ':
                    return board.convert_coords(i, loc)
        
        if board.n > 3 and moves < 4:
            move = random.randint(0, board.num_spaces - 1)
        else:
            move = minimax_2d(board, 0, -1000000, 1000000, False)[-1]
            print(move)
            #print(minimax_2d.cache_info())
    else:
        win, loc = board.almost_win_3d()
        print(str(win) + ', ' + str(loc))
        if win:
            if win == 'cross_dia':
                for i in range(board.n):
                    if loc == 0 and board.board[i][i][i] == ' ':
                        return board.convert_coords(i, i, i)
                    elif loc == 1 and board.board[i][max_index - i][i] == ' ':
                        return board.convert_coords(i, max_index - i, i)
                    elif loc == 2 and board.board[max_index - i][i][i] == ' ':
                        return board.convert_coords(max_index - i, i, i)
                    elif (loc == 3 and
                          board.board[max_index - i][max_index - i][i] == ' '):
                        return board.convert_coords(max_index - i,
                                                    max_index - i, i)
            
            for i in range(board.n):
                # TODO: CALCULATE SPACE NUMBERS
                if win == 'v_col' and board[i][loc[0]][loc[-1]] == ' ':
                    return board.convert_coords(i, loc[0], loc[-1])
                elif win == 'row' and board.board[loc[0]][loc[-1]][i] == ' ':
                    return board.convert_coords(loc[0], loc[-1], i)
                elif win == 'col' and board.board[loc[0]][i][loc[-1]] == ' ':
                    return board.convert_coords(loc[0], i, loc[-1])
                if win == 'dia':
                    if loc[-1] == 0 and board.board[loc[0]][i][i] == ' ':
                        return board.convert_coords(loc[0], i, i)
                    elif (loc[-1] == 1
                          and board.board[loc[0]][i][max_index - i] == ' '):
                        return board.convert_coords(loc[0], i, max_index - i)
                    elif loc[-1] == 2 and board.board[i][loc[0]][i] == ' ':
                        return board.convert_coords(i, loc[0], i)
                    elif (loc[-1] == 3
                          and board.board[i][loc[0]][max_index - i] == ' '):
                        return board.convert_coords(i, loc[0], max_index - i)
                    elif loc[-1] == 4 and board.board[i][i][loc[0]] == ' ':
                        return board.convert_coords(i, i, loc[0])
                    elif (loc[-1] == 5
                          and board.board[i][max_index - i][loc[0]] == ' '):
                        return board.convert_coords(i, max_index - i, loc[0])
        
        '''
        move = random.randint(1, board.num_spaces)
        i = int(move / (board.n**2))
        j = (int(move / board.n)) % board.n
        k = move % board.n
        '''
        move = minimax_3d(board, 0, -1000000, 1000000, False)[-1]
    
    return move

def play_3d(board):
    '''
    Function plays a game of n x n Tic Tac Toe
    Currently works for 2d
    '''
    clear()

    moves = 0
    winner = ' '

    print(board)

    while not board.check_win_3d() and moves < board.n**3:
        # Print the list of available spaces
        print('Available Spaces')
        for index in range(len(board.space_nums)):
            i = int(index / (board.n**2))
            j = (int(index / board.n)) % board.n
            k = index % board.n
            
            end_str = '  ' + '\n' * (((index + 1) % (board.n**2)) == 0)
            if board.board[i][j][k] == ' ':
                print(board.space_nums[index], end=end_str)
            else:
                print('  ', end=end_str)
        print()

        # Input validation for X's move (in case they mistype)
        valid = False
        while not valid:
            move = int(input('Type the name of the space you\'d'
                             + ' like to put an X in: '))
        
            clear()
            
            for index in range(len(board.space_nums)):
                i = int(index / (board.n**2))
                j = (int(index / board.n)) % board.n
                k = index % board.n
                
                if board.space_nums[index] == move and board.board[i][j][k] == ' ':
                    board.board[i][j][k] = 'X'
                    valid = True
                    moves += 1
                    break
                if valid:
                    break
                elif not valid and index == len(board.space_nums) - 1:
                    print('Invalid move!')
                    print(board)

        if board.check_win_3d() and moves >= 4:
            winner = 'X'
            break
        elif moves >= board.n**2:
            # If the board is filled, O also shouldn't go
            break
        else:
            winner = 'O'
            # Otherwise, let O go and input validate their move
            valid = False
            while not valid:
                move = player_o(board, moves)
                valid = board.move(move, 'O')

            moves += 1
            print(board)

    print(board)

    if moves < board.n**3:
        print(winner + ' won!')
    else:
        print('It\'s a tie!')



def play_2d(board):
    '''
    Function plays a game of n x n Tic Tac Toe
    Currently works for 2d
    '''
    clear()

    moves = 0
    winner = ' '

    print(board)

    while not board.check_win_2d() and moves < board.n**2:
        # Print the list of available spaces
        print('Available Spaces')
        for index in range(len(board.space_nums)):
            i = int(index / board.n)
            j = index % board.n
            end_str = '  ' + '\n' * (((index + 1) % board.n) == 0)
            if board.board[i][j] == ' ':
                print(board.space_nums[index], end=end_str)
            else:
                print('  ', end=end_str)
        print()

        # Input validation for X's move (in case they mistype)
        valid = False
        while not valid:
            move = int(input('Type the name of the space you\'d'
                             + ' like to put an X in: '))
            clear()
            
            valid = board.move(move - 1, 'X')
            if valid:
                break
            elif not valid:
                print('Invalid move!')
                print(board)

        moves += 1
        
        if board.check_win_2d() and moves >= 4:
            break
        elif moves >= board.n**2:
            # If the board is full, O also shouldn't go
            break
        else:
            # Otherwise, let O go and input validate their move
            valid = False
            while not valid:
                move = player_o(board, moves)
                valid = board.move(move, 'O')

            moves += 1
            print(board)

    print(board)

    if moves < board.n**2:
        print(board.check_win_2d() + ' won!')
    else:
        print('It\'s a tie!')


def main():
    print('Welcome to n x n Tic Tac Toe!')
    dimensions = int(input('Enter the number of dimensions to'
                           + 'play in (2 or 3): '))
    n = int(input('Enter a value for n (less than 10 for 2D, '
                  + 'less than 5 for 3D: '))
    board = b.Board(dimensions, n)

    if board.board:
        if board.dimensions == 3:
            play_3d(board)
        else:
            play_2d(board)

    play_again = input('Would you like to play again? ')
    if play_again[0].lower() == 'y':
        main()

if __name__ == '__main__':
    main()
