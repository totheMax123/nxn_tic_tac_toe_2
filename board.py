#########################
#
# n x n Tic Tac Toe Board
# Author: Max Dickman
#
# Program has board class
# for n x n and n x n x n
# tic tac toe
#
#########################

import print_board as pb

class Board(object):
    def __init__(self, dimensions, n):
        self.dimensions = dimensions
        self.n = n
        self.num_spaces = self.n**self.dimensions
        
        if dimensions == 2:
            self.board = [[' ' for j in range(n)] for i in range(n)]
        elif dimensions == 3:
            self.board = [[[' ' for k in range(n)] for j in range(n)] for i in range(n)]
        else:
            self.board = []

        self.linear_board = [' ' for i in range(self.num_spaces)]
        self.space_nums = [i + 1 for i in range(n**dimensions)]

    def __eq__(self, other):
        if not isinstance(other, Board):
            return False

        if other.dimensions != self.dimensions:
            return False

        if other.n != self.n:
            return False

        for i in range(self.num_spaces):
            if self.linear_board[i] != other.linear_board[i]:
                return False

        return True

    def __hash__(self):
        result = ''

        result = result.join(self.linear_board)
        
        result = result.replace('X', '1')
        result = result.replace('O', '2')
        result = result.replace(' ', '0')

        return int(result)

    def __repr__(self):
        if self.dimensions == 3:
            pb.print_board_3d(self.board, self.space_nums)
        else:
            pb.print_board_2d(self.board, self.space_nums)

        return ''

    def static_eval(self, depth, winner):
        if winner == 'X':
            return (self.num_spaces + 1) - depth
        elif winner == 'O':
            return -(self.num_spaces + 1) + depth
        else:
            return 0

    def convert_coords(self, i=-1, j=-1, k=-1):
        if self.dimensions == 3:
            space = i * self.n**2
            space += j * self.n
            space += k
        else:
            space = i * self.n
            space += j
        
        return space
                
    def move(self, pos, symbol):
        '''
        Function makes a move for any player (or a blank for minimax)
        Function then updates the linear board
        Returns the validity of the move
        '''
        if self.dimensions == 3:
            i = int(pos / (self.n**2))
            j = (int(pos / self.n)) % self.n
            k = pos % self.n

            if (self.board[i][j][k] == ' ' and symbol != ' ') or symbol == ' ':
                self.board[i][j][k] = symbol
                self.linear_board[pos] = symbol
            else:
                return False
        else:
            i = int(pos / self.n)
            j = pos % self.n

            if (self.board[i][j] == ' ' and symbol != ' ') or symbol == ' ':
                self.board[i][j] = symbol
                self.linear_board[pos] = symbol
            else:
                return False
        
        return True

    def check_win_2d(self, i=0):
        '''
        Code checks rows, then columns, then each diagonal for a win
        Works for any n x n board
        '''

        if self.dimensions == 3:
            full_board = self.board
            self.board = self.board[i]
        
        max_index = self.n - 1
        l_diagonal = []
        r_diagonal = []
        winning_lines = []
        
        for i in range(self.n):
            column = []
            row = []
            for j in range(self.n):
                column.append(self.board[j][i])
                row.append(self.board[i][j])
            winning_lines.append(column)
            winning_lines.append(row)
            l_diagonal.append(self.board[i][i])
            r_diagonal.append(self.board[i][max_index - i])

        winning_lines.append(l_diagonal)
        winning_lines.append(r_diagonal)

        if self.dimensions == 3:
            self.board = full_board

        for line in winning_lines:
            prev_space = line[0]
            win = True
            for space in line:
                if space != prev_space or space == ' ':
                    win = False
                    break
                prev_space = space
            
            if win:
                return space
        
        return None

    def check_win_3d(self):
        max_index = self.n - 1
        winner = None
        winning_lines = []
        lu_cross_diagonal = []
        ru_cross_diagonal = []
        ld_cross_diagonal = []
        rd_cross_diagonal = []
        
        for i in range(self.n):
            if winner == None:
                winner = self.check_win_2d(i)
            
            lu_cross_diagonal.append(self.board[i][i][i])
            # 1, 14, 27
            ru_cross_diagonal.append(self.board[i][i][max_index - i])
            # 3, 14, 25
            ld_cross_diagonal.append(self.board[i][max_index - i][max_index - i])
            # 19, 14, 9
            rd_cross_diagonal.append(self.board[max_index - i][i][max_index - i])
            # 21, 14, 7
            for j in range(self.n):
                column = []
                l_diagonal = []
                r_diagonal = []
                u_diagonal = []
                d_diagonal = []
                for k in range(self.n):
                    column.append(self.board[k][j][i])
                    l_diagonal.append(self.board[k][j][k])
                    r_diagonal.append(self.board[k][j][max_index - k])
                    u_diagonal.append(self.board[k][k][j])
                    d_diagonal.append(self.board[k][max_index - k][j])
                
                winning_lines.extend([column, l_diagonal, r_diagonal,
                                      u_diagonal, d_diagonal])
     
        winning_lines.extend([lu_cross_diagonal, ru_cross_diagonal,
                              ld_cross_diagonal, rd_cross_diagonal])
        
        for line in winning_lines:
            prev_space = line[0]
            win = True
            for space in line:
                if space != prev_space or space == ' ':
                    win = False
                    break
                prev_space = space

            if win:
                winner = space
                
        return winner

    def almost_win_2d(self, i=0, send_sums=False):
        max_index = self.n - 1
        
        if self.dimensions == 3:
            full_board = self.board
            self.board = self.board[i]
        
        row_sums = [0 for i in range(self.n)]
        col_sums = [0 for i in range(self.n)]
        diag_sums = [0, 0]

        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] == 'O':
                    col_sums[j] -= 1
                    row_sums[i] -= 1
                elif self.board[i][j] == 'X':
                    col_sums[j] += 1
                    row_sums[i] += 1

            if self.board[i][i] == 'O':
                diag_sums[0] -= 1
            elif self.board[i][i] == 'X':
                diag_sums[0] += 1

            if self.board[i][max_index - i] == 'O':
                diag_sums[1] -= 1
            elif self.board[i][max_index - i] == 'X':
                diag_sums[1] += 1

        if self.dimensions == 3:
            self.board = full_board

        if send_sums:
            return row_sums, col_sums, diag_sums

        for i in range(self.n):
            if row_sums[i] == max_index:
                return 'row', i
            elif col_sums[i] == max_index:
                return 'col', i

        for i in range(2):
            if diag_sums[i] == max_index:
                return 'dia', i

        return None, None

    def optimized_almost_win_2d(self, send_sums=False):
        board_str = str(self.__hash__())
        max_index = self.n - 1

        board_nums = [int(x) if x != '2' else -1 for x in board_str]
        board_nums = [[board_nums[i] for i in range(j * self.n,
                                                    (j + 1) * self.n)]
                      for j in range(0, self.n)]

        row_sums = [0 for i in range(self.n)]
        col_sums = [0 for i in range(self.n)]
        l_dia_sum = 0
        r_dia_sum = 0

        for i in range(self.n):
            for j in range(self.n):
                row_sums[i] += board_nums[i][j]
                col_sums[i] += board_nums[j][i]
            l_dia_sum += board_nums[i][i]
            r_dia_sum += board_nums[i][max_index - i]

        if send_sums:
            return row_sums, col_sums, [l_dia_sum, r_dia_sum]

        for i in range(self.n):
            if abs(row_sums[i]) == 2:
                return 'X' * (row_sums[i] > 0) + 'O' * (row_sums[i] < 0)
            if abs(col_sums[i]) == 2:
                return 'X' * (col_sums[i] > 0) + 'O' * (col_sums[i] < 0)

        if abs(l_dia_sum) == 2:
            return 'X' * (l_dia_sum > 0) + 'O' * (l_dia_sum < 0)
        if abs(r_dia_sum) == 2:
            return 'X' * (r_dia_sum > 0) + 'O' * (r_dia_sum < 0)

        return None

    def almost_win_3d(self, send_sums=False):
        max_index = self.n - 1
        ret = []
        for i in range(self.n):
            if send_sums:
                vals = self.almost_win_2d(i, True)
                for l in vals:
                    ret.append(l)
            else:
                win, loc = self.almost_win_2d(i)

                if win:
                    return win, [i, loc]

        col_sum = [0 for i in range(self.n**2)]
        dia_sum = [0 for i in range(4)]
        l_dia_sum = [0 for i in range(self.n)]
        r_dia_sum = [0 for i in range(self.n)]
        u_dia_sum = [0 for i in range(self.n)]
        d_dia_sum = [0 for i in range(self.n)]
        
        for i in range(self.n):
            for j in range(self.n):
                for k in range(self.n):
                    if self.board[k][j][i] == 'X':
                        col_sum[j * self.n + k] += 1
                    elif self.board[k][j][i] == 'O':
                        col_sum[j * self.n + k] -= 1

                if self.board[j][i][j] == 'X':
                    l_dia_sum[i] += 1
                elif self.board[j][i][j] == 'O':
                    l_dia_sum[i] -= 1
                    
                if self.board[j][i][max_index - j] == 'X':
                    r_dia_sum[i] += 1
                elif self.board[j][i][max_index - j] == 'O':
                    r_dia_sum[i] -= 1

                if self.board[j][j][i] == 'X':
                    u_dia_sum[i] += 1
                elif self.board[j][j][i] == 'O':
                    u_dia_sum[i] -= 1

                if self.board[j][max_index - j][i] == 'X':
                    d_dia_sum[i] += 1
                elif self.board[j][max_index - j][i] == 'O':
                    d_dia_sum[i] -= 1

            if self.board[i][i][i] == 'X':
                dia_sum[0] += 1
            elif self.board[i][i][i] == 'O':
                dia_sum[0] -= 1
            
            if self.board[i][max_index - i][i] == 'X':
                dia_sum[1] += 1
            elif self.board[i][max_index - i][i] == 'O':
                dia_sum[1] -= 1

            if self.board[max_index - i][i][i] == 'X':
                dia_sum[2] += 1
            elif self.board[max_index - i][i][i] == 'O':
                dia_sum[2] -= 1

            if self.board[max_index - i][max_index - i][i] == 'X':
                dia_sum[3] += 1
            elif self.board[max_index - i][max_index - i][i] == 'O':
                dia_sum[3] -= 1

        if send_sums:
            ret.extend([col_sum, dia_sum, l_dia_sum, r_dia_sum, u_dia_sum,
                       d_dia_sum])
            return ret    

        for i in range(len(col_sum)):
            if col_sum[i] == max_index:
                loc = int(i/self.n)
                j = i % self.n
                return 'v_col', [loc, j]

        for i in range(len(dia_sum)):
            if dia_sum[i] == max_index:
                return 'cross_dia', i

        for i in range(len(l_dia_sum)):
            if l_dia_sum[i] == max_index:
                return 'dia', [i, 2]
            if r_dia_sum[i] == max_index:
                return 'dia', [i, 3]
            if u_dia_sum[i] == max_index:
                return 'dia', [i, 4]
            if d_dia_sum[i] == max_index:
                return 'dia', [i, 5]

        return None, None

    def heuristic_eval(self, move, player):
        max_index = self.n - 1
        
        if self.dimensions == 3:
            i = int(move / (self.n**2))
            j = (int(move / self.n)) % self.n
            k = move % self.n

            self.board[i][j][k] = player
            sums = self.almost_win_3d(send_sums=True)
            self.board[i][j][k] = ' '
        else:
            i = int(move / self.n)
            j = move % self.n
            
            self.board[i][j] = player
            sums = self.almost_win_2d(send_sums=True)
            self.board[i][j] = ' '
        
        total = sum([x for sublist in sums for x in sublist])

        return {move: total}

if __name__ == '__main__':
    # Test code. Don't want this to run when imported
    #board = Board(3, 3)
    #print(board.convert_coords(0, 1, 1))
    import cProfile
    
    b1 = Board(2, 4)
    b1.move(0, 'O')
    #b1.move(4, 'X')
    b1.move(1, 'O')
    b1.move(2, 'O')
    print(b1)
    print(b1.optimized_almost_win_2d())
    print(cProfile.run('b1.heuristic_eval(1, \'X\')'))
    
    '''
    b1 = Board(3, 3)
    b1.board[0][1][1] = 'X'
    evals = {}
    for i in range(27):
        m1 = int(i / (b1.n**2))
        m2 = (int(i / b1.n)) % b1.n
        m3 = i % b1.n
        
        if b1.board[m1][m2][m3] == ' ':
            evals.update(b1.heuristic_eval(i, 'O'))
    
    print(evals)
    order = sorted(evals, key=evals.get)
    print(order)
    '''  

        
