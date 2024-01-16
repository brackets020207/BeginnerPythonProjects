import random
import time, os

def clear():
    os.system('cls')

DEAD = 0
LIVE = 1

def random_state(width, height):
    state = [DEAD, LIVE]
    return [[random.choice(state) for _ in range(height)] for _ in range(width)]

def render(board):
    print('_' * ((len(board[0])+2)*2))

    for i in board:
        print('|', end ='')
        for j in i:
        
            if j == 0:
                print(' '*2, end = '')
            else:
                print(u"\u2588"*2, end = '')
        print('|')
    print('-'* ((len(board[0])+2)*2))

def next_board_state(board):
    width = len(board)
    height = len(board[0])
    new = random_state(width, height)

    for i in range(width):
        for j in range(height):
            new[i][j] = new_cell(board, [i,j])
    
    return new

def day_and_night(board):
    width = len(board)
    height = len(board[0])
    new = random_state(width, height)

    for i in range(width):
        for j in range(height):
            new[i][j] = day_cell(board, [i,j])
    
    return new

def day_cell(board, cords):
    width = len(board)
    height = len(board[0])
    x = cords[0]
    y = cords[1]

    neighbour_count = 0 
    for i in range((x-1), (x+2)):
        if i < 0 or i >= width: continue
        for j in range((y-1), (y+2)):
            if j < 0 or j >= height: continue
            if i == x and j == y: continue
            if board[i][j] == LIVE:
                neighbour_count += 1
    
    lives = [3,6,7,8]
    
    if neighbour_count in lives:
        return LIVE
    else:
        return DEAD



def new_cell(board, cords):
    width = len(board)
    height = len(board[0])
    x = cords[0]
    y = cords[1]

    neighbour_count = 0 
    for i in range((x-1), (x+2)):
        if i < 0 or i >= width: continue
        for j in range((y-1), (y+2)):
            if j < 0 or j >= height: continue
            if i == x and j == y: continue
            if board[i][j] == LIVE:
                neighbour_count += 1
    
    
    
    if board[x][y] == LIVE:
        if neighbour_count <= 1:
            return DEAD
        elif neighbour_count <= 3:
            return LIVE
        else:
            return DEAD
    elif board[x][y] == DEAD:
        if neighbour_count == 3:
            return LIVE
        else:
            return DEAD

        

    



start = random_state(30, 75)


def run(start):
    while True:
        render(start)
        start = next_board_state(start)
        time.sleep(0.1)
        clear()

def run_day(start):
    while True:
        render(start)
        start = day_and_night(start)
        time.sleep(0.1)
        clear()



def load(filename):
    with open(filename, 'r') as state:
        init_state = state.read()
    init_state = init_state.split('\n')
    
    for i in range(len(init_state)):
        init_state[i] = list(init_state[i])
    
    for i in range(len(init_state)):
        for j in range(len(init_state[i])):
            init_state[i][j] = int(init_state[i][j])
    
    return init_state

def main():
    print('''GAME OF LIFE
------------
--> soup
--> day and night (dan)
--> gospel glider gun (ggg)
--> glider
--> toad
--> blinker''')
    runner = input('> ')
    if runner == 'soup':
        state = random_state(35, 75)
        run(state)
    
    elif runner == 'dan':
        state = random_state(35, 75)
        run_day(state)
    
    else:
        try:
            run(load(runner+'.txt'))
        
        except FileNotFoundError:
            print('Not an option')
            main()

if __name__ == "__main__":
    main()
    
