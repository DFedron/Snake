#import pygame as pg
#font = pygame.font.SysFont('arial', 20)
import random as r
import time as t
import turtle as gfx 

# Initialize list of body parts
body = []

# Define functons for movement bindings, each direction separated into individual movements to stop 180 turns
def head_up():

    if head.direction != "down":
        head.direction = "up"

def head_down():

    if head.direction != "up":
        head.direction = "down"

def head_left():

    if head.direction != "right":
        head.direction = "left"

def head_right():

    if head.direction != "left":
        head.direction = "right"

# Set global variables

delay = 0.1 # The lower the delay, the faster the game moves. This is to ensure dynamic difficulty and make sure the AI is actually improving
randMove = 50 # Sets the chance that the snake decides to move per state (0 indicates snake never moves, 100 indicates snake always tries to change direction)
randTurn = randMove / 2 # Sets the chance of which direction the snake moves (lower half makes the snake turn left, higher half makes the snake turn right)

attempt = 1 # Keep track of the attempt/epoch number
score = 0 # Keep track of the score 

#-- Set up the scoreboard UI
scoreboard = gfx.Turtle()

scoreboard.speed(0)
scoreboard.shape("square")
scoreboard.color("white")
scoreboard.penup()

scoreboard.hideturtle()

scoreboard.goto(0, 210)
scoreboard.write("Attempt: 0  Score: 0", align="center", font=("Arial", 20, "normal"))

#-- Set up the screen and its size
screen = gfx.Screen()
screen.tracer(0) # This eliminates gfx lib's automatic screen updates

screen.setup(width = 500, height = 500)
screen.title("Snake - Player Version")
screen.bgcolor("black")

# Set up keyboard bindings tied to the screen
screen.listen()

screen.onkeypress(head_up, "Up")
screen.onkeypress(head_down, "Down")
screen.onkeypress(head_left, "Left")
screen.onkeypress(head_right, "Right")
#--

#-- Initialize the head of the snake and its graphics
head = gfx.Turtle()

head.speed(0) 
head.shape("square")
head.color("orange")
head.penup()

head.goto(0,0) # Put the head at the center of the screen
head.direction = "stop" # Make it not move until player input tells it to move

def move_head(): # Check which direction the head is facing and set the position accordingly

    if head.direction == "up":
    
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
    
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
    
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
    
        x = head.xcor()
        head.setx(x + 20)
#--

#-- Set up initial pellet position as well as pellet graphics
pellet = gfx.Turtle()

pellet.speed(0)
pellet.shape("circle")
pellet.color("blue")

pellet.penup()
pellet.goto(0,100)
#--

# Driver code 
while True:

    # Determine whether the snake agent will randomly change direction or not
    moveChance = r.randint(1, 100)
    if(moveChance <= randMove):

         # If snake is determined to change direction, change direction according to the value generated and direction of the snake
        if(head.direction == "up"):
            if(randMove <= randTurn):
                head.direction = "left"
            else:
                head.direction = "right"
        
        elif(head.direction == "left"):
            if(randMove <= randTurn):
                head.direction = "down"
            else:
                head.direction = "up"
        
        elif(head.direction == "down"):
            if(randMove <= randTurn):
                head.direction = "right"
            else:
                head.direction = "left"
        
        else:
            if(randMove <= randTurn):
                head.direction = "up"
            else:
                head.direction = "down"

    screen.update()

    # Base case: the head collided with the edge of the screen at 250 or -250
    if head.xcor() > 240 or head.xcor() < -240 or head.ycor() > 240 or head.ycor() < -240:
        
        t.sleep(1) # Sleep program for one second to give feedback that collision happened
        
        head.goto(0,0)
        head.direction = "stop"

        # Body stays on screen unless moved even if cleared, so moved out of bounds
        for part in body:
            part.goto(1000, 1000)
        
        # Clear the list of body parts
        body.clear()

        # Reset game speed and score, print result to console
        delay = 0.1
        
        print(f'Attempt: {attempt} Score: {score}')
        
        score = 0
        attempt += 1


        scoreboard.clear()
        scoreboard.write("Attempt: {}  Score: {}".format(attempt, score), align="center", font=("Arial", 20, "normal")) 


    # Check if the snake head picked up a pellet
    if head.distance(pellet) < 20:
        
        # Move the pellet to a random area on the screen
        x = r.randint(-235, 235)
        y = r.randint(-235, 235)
        
        pellet.goto(x,y)

        # Add a body part
        new_part = gfx.Turtle()
        
        new_part.speed(0)
        new_part.shape("square")
        new_part.color("yellow")
        
        new_part.penup()
        
        body.append(new_part)

        # Increase the game speed by shortening the delay
        delay -= 0.001

        # Increase the score by 10
        score += 10
        
        scoreboard.clear()
        scoreboard.write("Attempt: {}  Score: {}".format(attempt, score), align="center", font=("Arial", 20, "normal")) 
    
    #--Body driver code below
    
    # Move the tail end first by moving in reverse order
    
    for index in range(len(body) - 1, 0, -1):
        
        x = body[index-1].xcor()
        y = body[index-1].ycor()
        
        body[index].goto(x, y)

    # Move the part to index 0
    
    if len(body) > 0:
    
        x = head.xcor()
        y = head.ycor()
        
        body[0].goto(x,y)

    move_head() # After these checks are completed, move the head

    # Check for a collision with a body part
    
    for part in body:
    
        if part.distance(head) < 20:
        
            t.sleep(1) # Sleep program for one second to give feedback that collision happened
        
            head.goto(0,0)
            head.direction = "stop"

            # Body stays on screen unless moved even if cleared, so moved out of bounds
            for part in body:
                part.goto(1000, 1000)
        
            # Clear the list of body parts
            body.clear()

            # Reset game speed and score, print result to console
            delay = 0.1
        
            print(f'Attempt: {attempt} Score: {score}')
        
            score = 0
            attempt += 1

            scoreboard.clear()
            scoreboard.write("Attempt: {}  Score: {}".format(attempt, score), align="center", font=("Arial", 20, "normal")) 

    t.sleep(delay) # The loop runs according to the current game speed
    
print("This message is stored in an unreachable part of the code. If it is printed, something is wrong.")