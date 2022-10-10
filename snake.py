
import random
import time
import math
import gym
import turtle as gfx
from gym.utils import seeding
from gym import spaces


HEIGHT = 20      # number of steps vertically from wall to wall of screen
WIDTH = 20       # number of steps horizontally from wall to wall of screen

class Snake(gym.Env):

    def __init__(self, isHuman=False, env_info={'state_space' : None}):
        super(Snake, self).__init__()

        self.done = False
        self.seed()
        self.reward = 0
        self.action_space = 4
        self.state_space = 12

        self.total = 0
        self.highest = 0
        self.human = isHuman
        self.env_info = env_info

        #-- Set up the screen and its size
        self.screen = gfx.Screen()
        self.screen.title("Snake - Player Version")
        self.screen.bgcolor('black')
        self.screen.tracer(0) # This eliminates gfx lib's automatic screen updates
        self.screen.setup(width=400+32, height=400+32)
        # Set up keyboard bindings tied to the screen
        self.screen.listen()
        self.screen.onkey(self.head_up, 'Up')
        self.screen.onkey(self.head_down, 'Down')
        self.screen.onkey(self.head_right, 'Right')
        self.screen.onkey(self.head_left, 'Left')     

        #-- Initialize the head of the snake and its graphics
        self.head = gfx.Turtle()
        self.head.shape('square')
        self.head.speed(0)
        self.head.penup()
        self.head.color("orange")
        self.head.goto(0, 0)    # Put the head at the center of the screen
        self.head.direction = 'stop'    # Make it not move until player input tells it to move
        # Initialize list of body parts
        self.body = []
        # self.addToBody()

   
        self.pellet = gfx.Turtle()
        self.pellet.speed(0)
        self.pellet.shape('circle')
        self.pellet.color('blue')
        self.pellet.penup()
    

        self.pellet.goto(0, 50)
        self.movePellet()
        # distance between apple and snake
        self.dist = self.head.distance(self.pellet)

        # score
        self.scoreboard = gfx.Turtle()
        self.scoreboard.speed(0)
        self.scoreboard.color('white')
        self.scoreboard.penup()
        self.scoreboard.hideturtle()
        self.scoreboard.goto(0, 180)
        self.scoreboard.write(f"Total: {self.total}   Highest: {self.highest}", align='center', font=('Arial', 18, 'normal'))

        # control
# Define functons for movement bindings, each direction separated into individual movements to stop 180 turns
    def head_up(self):
        if self.head.direction != "down":
            self.head.direction = "up"
    
    
    def head_down(self):
        if self.head.direction != "up":
            self.head.direction = "down"
    
    def head_left(self):
        if self.head.direction != "right":
            self.head.direction = "left" 
               

    def head_right(self):
        if self.head.direction != "left":
            self.head.direction = "right"

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]
    
    def move_head(self): # Check which direction the head is facing and set the position accordingly
        if self.head.direction == 'stop':
            self.reward = 0
        if self.head.direction == 'up':
            y = self.head.ycor()
            self.head.sety(y + 20)
        if self.head.direction == 'right':
            x = self.head.xcor()
            self.head.setx(x + 20)
        if self.head.direction == 'down':
            y = self.head.ycor()
            self.head.sety(y - 20)
        if self.head.direction == 'left':
            x = self.head.xcor()
            self.head.setx(x - 20)
        

    def movePellet(self):
        if self.head.distance(self.pellet) < 20:    
            self.pellet.x = round(random.randint(-10, 10) * 20)
            self.pellet.y = round(random.randint(-10, 10) * 20)
            self.pellet.goto(self.pellet.x, self.pellet.y)
            self.updateScore()
            self.addToBody()
            return True
        return False
   


    def updateScore(self):
        self.total += 1
        if self.total >= self.highest:
            self.highest = self.total

        self.scoreboard.clear()
        self.scoreboard.write(f"Total: {self.total}   Highest: {self.highest}", align='center', font=('Arial', 18, 'normal'))


    def resetScore(self):
        self.scoreboard.clear()
        self.total = 0
        self.scoreboard.write(f"Total: {self.total}   Highest: {self.highest}", align='center', font=('Arial', 18, 'normal'))
                    

    def addToBody(self):
        new_part = gfx.Turtle()
        new_part.speed(0)
        new_part.shape('square')
        new_part.color('yellow')
        new_part.penup()
        self.body.append(new_part)
        

    def move_body(self):

        for index in range(len(self.body)-1, 0, -1):
            x = self.body[index-1].xcor()
            y = self.body[index-1].ycor()
            self.body[index].goto(x, y)
        if len(self.body):
            self.body[0].goto(self.head.xcor(), self.head.ycor())
        
    
    def L2(self):
        self.prev_dist = self.dist
        self.dist = self.head.distance(self.pellet)


    def checkHitBody(self):
        if len(self.body) > 1:
            for body in self.body[1:]:
                if body.distance(self.head) < 20:
                    self.resetScore()
                    return True     

    def checkPellet(self):
        if len(self.body) > 0:
            for body in self.body[:]:
                if body.distance(self.pellet) < 20:
                    return True

    def checkWall(self):
        if self.head.xcor() > 200 or self.head.xcor() < -200 or self.head.ycor() > 200 or self.head.ycor() < -200:
            self.resetScore()
            return True
    
    def reset(self):
        if self.human:
            time.sleep(1)
        for body in self.body:
            body.goto(1000, 1000)

        self.body = []
        self.head.goto(0, 0)
        self.head.direction = 'stop'
        self.reward = 0
        self.total = 0
        self.done = False

        state = self.getState()

        return state


    def game(self):
        reward = False
        self.screen.update()
        self.move_head()

        if self.movePellet():
            self.reward = 10
            reward = True

        self.move_body()
        self.L2()
        #If hit body, gameover
        if self.checkHitBody():
            self.reward = -100
            reward = True
            self.done = True
            if self.human:
                self.reset()
       #If hit wall, gameover
        if self.checkWall():
            self.reward = -100
            reward = True
            self.done = True
            if self.human:
                self.reset()

        if not reward:
            if self.dist < self.prev_dist:
                self.reward = 1
            else:
                self.reward = -1
        if self.human:
            time.sleep(0.25)
            state = self.getState()

    
    # AI agent
    def step(self, action):
        if action == 0:
            self.head_up()
        if action == 1:
            self.head_down()
        if action == 2:
            self.head_right()
        if action == 3:
            self.head_left()
        self.game()
        state = self.getState()
        return state, self.reward, self.done, {}


    def getState(self):
        # snake coordinates abs
        self.head.x, self.head.y = self.head.xcor()/WIDTH, self.head.ycor()/HEIGHT   
        # snake coordinates scaled 0-1
        self.head.xsc, self.head.ysc = self.head.x/WIDTH+0.5, self.head.y/HEIGHT+0.5
        # apple coordintes scaled 0-1 
        self.pellet.x, self.pellet.y = self.pellet.xcor()/WIDTH, self.pellet.ycor()/HEIGHT
        self.pellet.xsc, self.pellet.ysc = self.pellet.x/WIDTH+0.5, self.pellet.y/HEIGHT+0.5

        # wall check
        if self.head.y >= HEIGHT/2:
            wall_up, wall_down = 1, 0
        elif self.head.y <= -HEIGHT/2:
            wall_up, wall_down = 0, 1
        else:
            wall_up, wall_down = 0, 0
        if self.head.x >= WIDTH/2:
            wall_right, wall_left = 1, 0
        elif self.head.x <= -WIDTH/2:
            wall_right, wall_left = 0, 1
        else:
            wall_right, wall_left = 0, 0

        # body close
        body_up = []
        body_right = []
        body_down = []
        body_left = []
        if len(self.body) > 3:
            for body in self.body[3:]:
                if body.distance(self.head) == 20:
                    if body.ycor() < self.head.ycor():
                        body_down.append(1)
                    elif body.ycor() > self.head.ycor():
                        body_up.append(1)
                    if body.xcor() < self.head.xcor():
                        body_left.append(1)
                    elif body.xcor() > self.head.xcor():
                        body_right.append(1)
        
        if len(body_up) > 0: body_up = 1
        else: body_up = 0
        if len(body_right) > 0: body_right = 1
        else: body_right = 0
        if len(body_down) > 0: body_down = 1
        else: body_down = 0
        if len(body_left) > 0: body_left = 1
        else: body_left = 0

      
        state = []
        if self.env_info['state_space'] == 'coordinates':
            state.append(self.pellet.xsc)
            state.append(self.pellet.ysc)
            state.append(self.head.xsc)
            state.append(self.head.ysc)
            state.append(int(wall_up or body_up))
            state.append(int(wall_right or body_right))
            state.append(int(wall_down or body_down))
            state.append(int(wall_left or body_left))
            state.append(int(self.head.direction == 'up'))
            state.append(int(self.head.direction == 'right'))
            state.append(int(self.head.direction == 'down'))
            state.append(int(self.head.direction == 'left'))


 
        elif self.env_info['state_space'] == 'no direction':
            state.append(int(self.head.y < self.pellet.y))
            state.append(int(self.head.x < self.pellet.x))
            state.append(int(self.head.y > self.pellet.y))
            state.append(int(self.head.x > self.pellet.x))
            state.append(int(wall_up or body_up))
            state.append(int(wall_right or body_right))
            state.append(int(wall_down or body_down))
            state.append(int(wall_left or body_left))
            state.append(0)
            state.append(0)
            state.append(0)
            state.append(0)



    
        elif self.env_info['state_space'] == 'no body knowledge':
            state.append(int(self.head.y < self.pellet.y))
            state.append(int(self.head.x < self.pellet.x))
            state.append(int(self.head.y > self.pellet.y))
            state.append(int(self.head.x > self.pellet.x))
            state.append(wall_up)
            state.append(wall_right)
            state.append(wall_down)
            state.append(wall_left)
            state.append(int(self.head.direction == 'up'))
            state.append(int(self.head.direction == 'right'))
            state.append(int(self.head.direction == 'down'))
            state.append(int(self.head.direction == 'left'))
 
 
        
        else:
            state.append(int(self.head.y < self.pellet.y))
            state.append(int(self.head.x < self.pellet.x))
            state.append(int(self.head.y > self.pellet.y))
            state.append(int(self.head.x > self.pellet.x))
            state.append(int(wall_up or body_up))
            state.append(int(wall_right or body_right))
            state.append(int(wall_down or body_down))
            state.append(int(wall_left or body_left))
            state.append(int(self.head.direction == 'up'))
            state.append(int(self.head.direction == 'right'))
            state.append(int(self.head.direction == 'down'))
            state.append(int(self.head.direction == 'left'))        
              

        return state

if __name__ == '__main__':   
    env = Snake(isHuman = True)
    while True:
        env.game()
    print("This message is stored in an unreachable part of the code. If it is printed, something is wrong.")
