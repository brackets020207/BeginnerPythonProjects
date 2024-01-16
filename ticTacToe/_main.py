import random
import time
import os
import sys

sys.setrecursionlimit(1500)

class InvalidMove(Exception):
    pass

def clear():
    os.system('cls')

def make_board():
    return [[None for i in range(3)] for j in range(3)]

def render(board):
    print('    0 1 2 ')
    print('   ------- ')
    for i in range(len(board)):
        print(i, '|', end = ' ')
        for j in range(len(board)):
            if board[i][j] == None:
                print(' ', end =' ')
            else:
                print(board[i][j], end =' ')
            
        print('|')
    print('   ------- ')

def get_move(board, side):
    while True:
        coordinates = input().split()
        valid = ['0', '1', '2']
        if len(coordinates) != 2 or coordinates[0] not in valid or coordinates[1] not in valid:
            print('Invalid move')
            continue
        else:
            return (int(coordinates[0]), int(coordinates[1]))

def make_move(board, coords, side):
    new = make_board()
    for i in range(len(board)):
        for j in range(len(board[i])):
            new[i][j] = board[i][j]
    x = coords[0]
    y = coords[1]
    if board[x][y] != None:
        raise InvalidMove("Move was invalid")
    new[x][y] = side
    return new 

def move_is_valid(board, coords):
    x = coords[0]
    y = coords[1]
    if board[x][y] != None:
        return False
    else:
        return True

def get_winner(board):
    lines = get_all_lines(board)
    for line in lines:
        linevalues = [board[x][y] for (x,y) in line]
        if len(set(linevalues)) == 1 and linevalues[0] is not None:
            return linevalues[0]
        
    return None

def get_all_lines(board):
    rows = []
    for i in range(len(board)):
        row = []
        for j in range(len(board[i])):
            row.append((i, j))
        rows.append(row)
    
    cols = []
    for i in range(len(board)):
        col = []
        for j in range(len(board)):
            col.append((j, i))
        cols.append(col)
    
    diagonals = [[(0,0), (1,1), (2,2)],
                 [(2,0), (1,1), (0,2)]]
    
    return rows + cols + diagonals

def board_is_full(board):
    for i in board:
        for j in i:
            if not j:
                return False
    return True
     

def play(players):
    clear()
    X = 'X'
    O = '0'
    playerguide = {'1': get_move, '2':get_random_move, '3':get_winning_ai_move, '4':get_block_ai_move, '5': minimax_move}
    p1 = playerguide[players[0]]
    p2 = playerguide[players[1]]
    
    board = make_board()
    render(board)
    keys = [X, O]

    turn = 0
    while True:
        player = keys[turn%2]
        print(player + "'s turn")
        time.sleep(0.5)
        if player == X:
            move = p1(board, player)
        elif player == O:
            move = p2(board, player)

        if move_is_valid(board, move):
            board = make_move(board, move, player)
        else:
            print('Invalid move')
            continue
        clear()
        render(board)

        if get_winner(board):
            print(get_winner(board), ' has won!')
            play_again(play, players)
        
        elif board_is_full(board):
            print("It's a draw")
            play_again(play, players)
        
        
        turn +=1

def get_board_string(board):
    string = ''
    for i in board:
        for j in i:
            string = string+str(j)

    return string


        
def play_again(func, args):
    print('Would you like to play again?')
    playagain = input()

    if playagain.startswith('y'):
        clear()
        func(args)
    else:
        time.sleep(1)
        clear()
        play(menu())
        



def get_valid_moves(board):
    moves = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if not board[i][j]:
                moves.append((i, j))
    
    return moves

def get_winning_moves(board, side):
    lines = get_all_lines(board)
    winners = []
    for line in lines:
        linevalues = [board[x][y] for (x,y) in line]
        if len(set(linevalues)) == 2 and linevalues.count(side) == 2:
            for (x,y) in line:
                if board[x][y] == None:
                    winners.append((x,y))
    
    return winners

def get_winning_ai_move(board, side):
    if get_winning_moves(board, side):
        return random.choice(get_winning_moves(board, side))
    
    else:
        return get_random_move(board, side)

def get_block_ai_move(board, side):
    inversion = {'0': 'X', 'X': '0'}
    if get_winning_moves(board, side):
        return random.choice(get_winning_moves(board, side))
    
    elif get_winning_moves(board, inversion[side]):
        return random.choice(get_winning_moves(board, inversion[side]))
    
    else:
        return get_random_move(board, side)
    


def get_random_move(board, side):
    moves = get_valid_moves(board)
    coords = random.choice(moves)
    return coords

def menu():
    print('TicTacToe')
    print('List of players - Enter players by number code separated by a space')
    print('----------------')
    print('1 - < Human >')
    print('2 - < AI - Easy >')
    print('3 - < AI - Better than Easy but worse than Medium >')
    print('4 - < AI - Medium >')
    print('5 - < AI - Impossible >')
    print('Anything Else - < Quit >')
    
    validsetting = '1 2 3 4 5'.split()
    while True:
        setting = input()     
        try:
            p1, p2 = setting.split()
        except:
            sys.exit()

        if p1 not in validsetting or p2 not in validsetting:
            print('Invalid player(s)')
            continue

        else:
            return p1,p2
        
def get_opponent(player):
    inversion = {'0': 'X', 'X': '0'}
    return inversion[player]

def minimax_move(board, who_am_i):
    best_move = None
    best_score = None

    for move in get_valid_moves(board):
        _board = make_move( board, move, who_am_i)

        opp = get_opponent(who_am_i)
        score = minimax_score(_board, opp, who_am_i)
        if best_score is None or score > best_score:
            best_move = move
            best_score = score

    return best_move


def minimax_score(board, player_to_move, player_to_optimize):
    winner = get_winner(board)
    if winner is not None:
        if winner == player_to_optimize:
            return 10
        else:
            return -10
    elif board_is_full(board):
        return 0

    legal_moves = get_valid_moves(board)

    scores = []
    for move in legal_moves:
        _board = make_move(board, move, player_to_move)

        opp = get_opponent(player_to_move)
        opp_best_response_score = minimax_score(_board, opp, player_to_optimize)
        scores.append(opp_best_response_score)

    if player_to_move == player_to_optimize:
        return max(scores)
    else:
        return min(scores)    

if __name__ == "__main__":
    play(menu())
    


