import time, sys
import os
import random
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
def clear():
    os.system('cls')
class Snake:
    UP = (1, 0)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    def __init__(self, body, direction):
        self.body = body
        self.direction = direction
    
    def take_step(self, position):
        self.body.pop(0)
        self.body.append(position)

    def set_direction(self, direction):
        self.direction = direction

    def extend(self, position):
        self.body.append(position)

    def head(self):
        return self.body[-1]

class Game:
    empty = 0
    body = 1
    head = 2
    apple = 3
    score = 0

    def __init__(self, height, width):
        self.width = width
        self.height = height
        self.snake = Snake([(0, 0),(0, 1),(0, 2),(0, 3),(1, 3),(2, 3),(2, 4)], UP)
        self.apple = Apple((random.randint(0, height-1), random.randint(0,width-1)))
    
    def play(self):
        self.render()
        while True:
            direction = input().lower()
            

        
            if direction == 'w' and self.snake.direction != DOWN:
                self.snake.set_direction(UP)
            elif direction == 'a' and self.snake.direction != RIGHT:
                self.snake.set_direction(LEFT)
            elif direction == 's' and self.snake.direction != UP:
                self.snake.set_direction(DOWN)
            elif direction == 'd' and self.snake.direction != LEFT:
                self.snake.set_direction(RIGHT)

            next_pos = self.get_next_position(self.snake.head(), self.snake.direction)
            if next_pos in self.snake.body:
                print('Game Over')
                print(f"score: {self.score}")
                yes=input()
                break
            elif next_pos == self.apple.position:
                self.apple.position = (random.randint(0, self.height-1), random.randint(0,self.width-1))
                self.score+=1
                self.snake.extend(next_pos)


            else:
                self.snake.take_step(next_pos)

            clear()
            self.render()

    
    def create_matrix(self):
        matrix = [[self.empty for i in range(self.width)] for i in range(self.height)]
        apple = self.apple.position
        

        matrix[apple[0]][apple[1]] =self.apple
        
        for co in self.snake.body:
            matrix[co[0]][co[1]] = self.body
        
        head = self.snake.head()
        
        matrix[head[0]][head[1]] = self.head
        return matrix


    def render(self):
        matrix = self.create_matrix()
        display = {self.empty: ' ',
                   self.body: '0',
                   self.head: 'X',
                   self.apple: '*'}

        top = '+'+('-'*self.width) + '+'
        print(top)
        for i in range(len(matrix)):
            line = '|'
            for j in range(len(matrix[i])):

                line+=display[matrix[i][j]]
            line+='|'
            print(line)
        print(top)
            
    def get_next_position(self, position, direction):
        x = (position[0] + direction[0]) % self.height
        y = (position[1] + direction[1]) % self.width
        return (x,y)




class Apple:
    def __init__(self, position):
        self.position = position

game = Game(10, 20)
game.play()



