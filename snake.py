import pygame
import time
import random
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT

hsFile = open('highscore.txt', 'r')
HIGHSCORE = int(hsFile.read())
hsFile.close()
# colors used
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# size of one block
SIZE = 20

# class for food of the snake
class Food:
    def __init__(self, win):
        self.win= win
        self.x= 60
        self.y= 60
        self.width= 20
        self.height= 20
        self.radius=7.5

    def draw(self):
        self.win.fill(RED,(self.x, self.y, self.width, self.height))
        pygame.display.update()

    def move(self):
        # Draw food on random positions
        self.x = random.randint(1, 24)*SIZE
        self.y = random.randint(1, 24)*SIZE


class Snake:
    # snakeleftpics=[]
    # snakerightpics=[]
    
    def __init__(self, win, length):
        self.score= 0
        self.length = length
        self.win= win
        self.x= [SIZE]*length
        self.y= [SIZE]*length
        self.width= 20
        self.height= 20
        self.vel= 5
        self.direction = 'none'

    def draw(self):
        # draw the snake and keep displaying the score
        self.win.fill(BLACK)
        pygame.draw.rect(self.win,WHITE,(0, 500, 500, 0),width=1)
        font1= pygame.font.SysFont('comicsans', 20, True)
        text1= font1.render('Score: '+str(self.score)+'', 1, (255, 255, 255))
        text2= font1.render('High Score: '+str(HIGHSCORE)+'', 1, (255, 255, 255))
        self.win.blit(text1, ((250 - text1.get_width()/2,520 - text1.get_height()/2)))
        self.win.blit(text2, ((250 - text2.get_width()/2,520 + text1.get_height() - text2.get_height()/2)))

        for i in range(self.length):
            self.win.fill(GREEN,(self.x[i], self.y[i], self.width, self.height))

        self.win.fill(BLUE,(self.x[0], self.y[0], self.width, self.height))

        pygame.display.update()

    # Increase length of snake everytime it collects the food
    def inc_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)
        return self.length

    def move(self):
        # move the snake based on arrow keys
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'up':
            self.y[0] -= SIZE
            if self.y[0] <= -SIZE:
                self.y[0] = 480

        if self.direction == 'down':
            self.y[0] += SIZE
            if self.y[0] >= 500:
                self.y[0] = 0

        if self.direction == 'left':
            self.x[0] -= SIZE
            if self.x[0] <= -SIZE:
                self.x[0] = 480

        if self.direction == 'right':
            self.x[0] += SIZE
            if self.x[0] >= 500:
                self.x[0] = 0

        self.draw()


class Game:
    # Initiate the game.
    # Draw the window (500x600).
    def __init__(self):
        pygame.init()
        self.winWidth = 500
        self.winHeight = 600
        self.win= pygame.display.set_mode((self.winWidth,self.winHeight))
        self.win.fill(BLACK)
        pygame.display.set_caption("Snake")

        self.food = Food(self.win)
        self.food.draw()

        self.snake = Snake(self.win, 1)
        self.snake.draw()

        pygame.draw.rect(self.win,WHITE,(0, 500, self.winWidth, 0),width=1)
        font1= pygame.font.SysFont('comicsans', 20, True)
        text1= font1.render('Score: '+str(self.snake.score)+'', 1, (255, 255, 255))
        text2= font1.render('High Score: '+str(HIGHSCORE)+'', 1, (255, 255, 255))
        self.win.blit(text1, ((250 - text1.get_width()/2,520 - text1.get_height()/2)))
        self.win.blit(text2, ((250 - text2.get_width()/2,520 + text1.get_height() - text2.get_height()/2)))
        pygame.display.update()

    def crash(self, len):
        # When the snake crashes into itself, the game is over.
        # The highscore is updated accordingly.
        for i in range(3,len):
            if self.snake.x[0] == self.snake.x[i]:
                if self.snake.y[0] == self.snake.y[i]:
                    pygame.time.delay(1000)
                    self.win.fill(BLACK)
                    fontOver= pygame.font.SysFont('comicsans', 45, True)
                    label = fontOver.render('GAME OVER :(', 1, WHITE)
                    self.win.blit(label, (250 - label.get_width() / 2, 300 - label.get_height() / 2))
                    pygame.display.update()
                    if self.snake.score >= HIGHSCORE:
                        print('new high score: ', self.snake.score)
                        f1 = open('highscore.txt', 'w')
                        f1.write(str(self.snake.score))
                        f1.close()
                        pygame.time.delay(1000)
                        self.win.fill(BLACK)
                        fontHS= pygame.font.SysFont('comicsans', 40, True)
                        labelHS = fontHS.render('NEW HIGHSCORE!!!', 1, WHITE)
                        self.win.blit(labelHS, (250 - labelHS.get_width() / 2, 300 - labelHS.get_height() / 2))
                        pygame.display.update()
                    time.sleep(2)
                    pygame.quit()

    # Method to check if the snake has collected its food.
    def collectFood(self):
        if self.snake.x[0] < self.food.x + SIZE and self.snake.x[0] >= self.food.x:
            if self.snake.y[0] < self.food.y + SIZE and self.snake.y[0] >= self.food.y:
                self.snake.score+=50
                newlen = self.snake.inc_length()
                self.food.move()
                for i in range(newlen):
                    while(self.snake.x[i] == self.food.x and self.snake.y[i] == self.food.y):
                        self.food.move()


    def run(self):
        # method used to run the game.
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    else:
                        if event.key == pygame.K_UP or K_DOWN or K_LEFT or K_RIGHT:
                            if event.key == pygame.K_UP:
                                if self.snake.direction == 'down':
                                    self.snake.direction = 'down'
                                else:
                                    self.snake.direction = 'up'

                            if event.key == pygame.K_DOWN:
                                if self.snake.direction == 'up':
                                    self.snake.direction = 'up'
                                else:
                                    self.snake.direction = 'down'

                            if event.key == pygame.K_LEFT:
                                if self.snake.direction == 'right':
                                    self.snake.direction = 'right'
                                else:
                                    self.snake.direction = 'left'

                            if event.key == pygame.K_RIGHT:
                                if self.snake.direction == 'left':
                                    self.snake.direction = 'left'
                                else:
                                    self.snake.direction = 'right'

            self.snake.move()
            self.food.draw()
            self.crash(self.snake.length)
            self.collectFood()

            time.sleep(0.1)

if __name__ == "__main__":
    game = Game()
    game.run()