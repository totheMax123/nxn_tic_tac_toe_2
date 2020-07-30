#########################
#
# n x n Tic Tac Toe Display
# Author: Max Dickman
#
# Program displays boards for
# n x n and n x n x n Tic Tac Toe
# Used in __repl__ function
# of the Board class
#
#########################

def print_board_2d(board, space_nums):
    '''
    Function prints the contents of the board with some ASCII art
    Works for 2 dimensional boards
    '''

    vbar = '   |'
    spacer = ' '
    hbar = '--+-'
    start_hbar = '-'
    end_hbar = '--'

    if len(space_nums) >= 10:
        spacer = '  '
        vbar = '    |'
        hbar = '--+--'
        start_hbar = '--'
        end_hbar = '--'
    
    for i in range(len(board)):
        print(' ' + vbar * (len(board) - 1))
        print(' ', end='')
        for j in range(len(board[i])):
            if space_nums[i * len(board) + j] >= 10 and board[i][j] == ' ':
                spacer = ' '
            elif len(space_nums) >= 10:
                spacer = '  '
            
            if board[i][j] == ' ':
                print(' ' + str(space_nums[i * len(board) + j])
                      + spacer, end='')
            else:
                print(' ' + board[i][j] + spacer, end='')

            if i == j == len(board) - 1:
                print()
            elif j == len(board) - 1:
                print('\n ' + vbar * (len(board) - 1))
                print(' '+ start_hbar + hbar * (len(board) - 1) + end_hbar)
            else:
                print('|', end='')
    print(' ' + vbar * (len(board) - 1))  
    print()

def print_board_3d(board, space_nums):
    '''
    Function prints the contents of the board with some ASCII art
    Works for 3 dimensional boards
    '''

    spacer = '  '
    vbar = '    |'
    hbar = '--+--'
    start_hbar = '--'
    end_hbar = '--'
    three_dim_spacer = '\t' * (6 - len(board)) * (len(board) != 0)

    for i in range(len(board)):
        for j in range(len(board[i])):
            print(' ' + three_dim_spacer * (len(board) - (i + 1)) +
                  vbar * (len(board[i][j]) - 1))
            print(' ' + three_dim_spacer * (len(board) - (i + 1)), end='')
            for k in range(len(board[i][j])):
                if space_nums[i * (len(board[i])**2)
                    + j * len(board[i][j]) + k] >= 10 and board[i][j][k] == ' ':
                    spacer = ' '
                elif len(space_nums) >= 10:
                    spacer = '  '
                
                if board[i][j][k] == ' ':
                    print(' ' + str(space_nums[i * (len(board[i])**2)
                                               + j * len(board[i][j]) + k])
                          + spacer, end='')
                else:
                    print(' ' + board[i][j][k] + spacer, end='')

                if j == k == len(board) - 1:
                    print()
                elif k == len(board) - 1:
                    print('\n ' + three_dim_spacer * (len(board) - (i + 1))
                          + vbar * (len(board[i][j]) - 1))
                    print(' ' + three_dim_spacer * (len(board) - (i + 1))
                          + start_hbar + hbar * (len(board[i][j]) - 1)
                          + end_hbar)
                else:
                    print('|', end='')
        print(' ' + three_dim_spacer * (len(board) - (i + 1))
              + vbar * (len(board[i][j]) - 1))
