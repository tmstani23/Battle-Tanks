import pygame
import time
import random

#this is a test of pygame

#initialize the pygame modules
#there are six so check init should return the initialized modules
#if pygame is correctly installed and initialized:
checkInit = pygame.init()
print(checkInit)

#define color variables:
bgrey = (24,51,49)
blue = (82,112,116)
lgrey = (163,181,166)
maroon = (128,0,0)

#define font variables:
tinyFont = pygame.font.SysFont("comicsansms", 12)
smallFont = pygame.font.SysFont("comicsansms", 25)
medFont = pygame.font.SysFont("comicsansms", 50)
largeFont = pygame.font.SysFont("comicsansms", 80)

#define screen width and height variables:
display_width = 800
display_height = 600

#define head block size
block_size = 20

#create variable that holds the size of the apple:
appleThickness = 30

#define snake's head image:
sh_image = pygame.image.load("c:/Tim's Files/my dream/learning/Programming/python/Snake Game/snakehead1.png")
#define apple image:
apple_image = pygame.image.load("c:/Tim's Files/my dream/learning/Programming/python/Snake Game/apple2.png")

#create the game surface with resolution of 800 x 600:
gameDisplay = pygame.display.set_mode((display_width, display_height))
#Set the game title on the top bar:
pygame.display.set_caption('Snake')

#incorporate game icon
icon = pygame.image.load("c:/Tim's Files/my dream/learning/Programming/python/Snake Game/gameicon.jpg")
pygame.display.set_icon(icon)
#define a clock variable that tracks time in the game loop
clock = pygame.time.Clock()
#head position variables:

#frames per second variable:
fps = 15

sDirection = "up"

#create screen message function:
def message_to_screen(msg, color, y_displace = 0, size = "small"):
    #create two variables that are now each text_objects functions:
    textSurf, textRect = text_objects(msg, color, size)
    #set textRect.center to = the center of the display:
    textRect.center = (display_width / 2), (display_height / 2 + y_displace)
    #display the two text objects to the screen:
    gameDisplay.blit(textSurf, textRect)

#create text object function that takes in message and color:    
def text_objects(msg, color, size):
    #If the argument input size = "tiny"
    if size == "tiny":
        #create variable that renders small font variable, msg and color
        textSurface = tinyFont.render(msg, True, color)
    elif size == "small":
        #create variable that renders small font variable, msg and color
        textSurface = smallFont.render(msg, True, color)
    elif size == "medium":
        #create variable that renders small font variable, msg and color
        textSurface = medFont.render(msg, True, color)
    elif size == "large":
        #create variable that renders small font variable, msg and color
        textSurface = largeFont.render(msg, True, color)
    #return the variable when text_objects is called
    return textSurface, textSurface.get_rect()

#create draw snake function:
def drawSnake(block_size, snakeList):
    #rotation direction of head when user presses specific direction key
    if sDirection == "right":
        head = pygame.transform.rotate(sh_image, 270)
    elif sDirection == "left":
        head = pygame.transform.rotate(sh_image, 90)
    elif sDirection == "up":
        head = sh_image
    elif sDirection == "down":
        head = pygame.transform.rotate(sh_image, 180)
    
    #display the head image at snakeList element locations:
    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))
    #go to snakeList for x and y positions:
    for XnY in snakeList[0:-1]:
        #draw a rectangle(where, color, [location,coords,width,height])
        #draw snake using the head_x head_y variable values for the x and y position
        #remember location of the snake head comes from snakeList
        pygame.draw.rect(gameDisplay, bgrey, [XnY[0], XnY[1], block_size, block_size])


#define the pause function
def pause():
    paused = True
    
    #display paused messages
    message_to_screen("Paused", blue, -100, size = "large")
    message_to_screen("Press 'C' to continue or 'Q' to quit", maroon, -20)
    #update the game with the changes
    pygame.display.update()
    #while the paused variable = True
    
    while paused:
        for event in pygame.event.get():
            #if X is clicked quit
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            #if a key is pressed down:
            if event.type == pygame.KEYDOWN:
                #if key is c paused = False so exit the loop
                if event.key == pygame.K_c:
                    paused = False
                #else if the q key: quit the game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
      
        #run 5 iterations of the loop
        clock.tick(5)

                
#define the score function:            
def score(score):
    #text variable uses smallFont function renders it with the message 
    #plus the string version of the score argument input
    text = smallFont.render("Score: " +str(score), True, bgrey)
    gameDisplay.blit(text, [0,0])

def randAppleGen():
        #generate a new apple in a random location:
        #remember that randapplex and y are called within the game loop,
        #below; when drawing the apple it references these two variables
        randAppleX = round(random.randrange(0, display_width - appleThickness))# / 10.0) * 10.0 
        randAppleY = round(random.randrange(0, display_height - appleThickness))# / 10.0) * 10.0
        return randAppleX, randAppleY

#define game intro screen function:
def gameIntro():
    intro = True
    
    #while loop that controls events that happen in the game intro screen
    while intro:
        #for any event that happens get the event from pygame library
        for event in pygame.event.get():
            #if user clicks the X to close the game:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            #if the key q is pressed:
            if event.type == pygame.KEYDOWN:
                #exit the gameover while loop and then exit the game
                if event.key == pygame.K_q:
                    pygame.quit
                    quit()
                if event.key == pygame.K_c:
                    #intro = false exits the game intro loop because the while loop 
                    #is dependent on intro being true
                    intro = False
        #fill the screen with a lgrey background
        gameDisplay.fill(lgrey)
        message_to_screen("Welcome to Snake", blue, -160, "large")
        message_to_screen("The objective of the game is to eat red apples.", bgrey, -80, "small")
        message_to_screen("The more apples you eat the longer you get.", bgrey, -40, "small")
        message_to_screen("If you run into yourself or the edge you die.", bgrey, 0, "small")
        message_to_screen("Press 'C' to play, 'P' to pause, or 'Q' to quit.", maroon, 60, "small")
        message_to_screen("Created by Timothy Stanislav; Indoorkin Productions", bgrey, 225, "tiny")

        #update and iterate clock tick at 15 fps
        pygame.display.update()
        clock.tick(fps)

        
#Create the primary game loop
#This loop runs while the game is being played
#It creates the background, the screen objects and 
#iterates the code over and over like a flip book animation
        
def gameLoop():
    gameExit = False
    gameOver = False
    #starts the head of the snake in the middle of the screen:
    head_x = display_width/2 
    head_y = display_height/2 
    #change amount variables represent change in position amount or,
    #how much the head x or y moves per tick
    head_x_change = 0
    head_y_change = 0
    #create snake list for storing head x and y positions:
    snakeList = []
    #set snake length variable
    snakeLength = 1
    #set variable for direction snake is heading:
    
    #set variables for x and y position of apple.  random location based on, 
    #the display width and height
    #see randAppleGen for the functionality of randAppleX,Y:  
    randAppleX, randAppleY = randAppleGen()

    
    #while game exit is false ie while the game is running:
    while not gameExit:
        
        if gameOver == True:
           
            #display 2 messages 
            message_to_screen("You lose!", blue, y_displace = -160, size = "large")
            message_to_screen("Press 'C' to play again or 'Q' to Quit.", 
            maroon, y_displace = -80, size = "small") 
            #update the game:
            pygame.display.update()
        
        #while game over:
        while gameOver == True:
            
            
            
            #get the event keydown from pygame module
            for event in pygame.event.get():
                #if user clicks the X to close the game:
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True
                #if the key q is pressed:
                elif event.type == pygame.KEYDOWN:
                    #exit the gameover while loop and then exit the game
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    #if c key is pressed exit gameOver while loop and go back to gameLoop
                    if event.key == pygame.K_c:
                        gameLoop()
                        gameOver = False

        #for a specific event do something:
        #these events are things like keypress down/up
        #mousebutton down/up, mouse position within or out etc
        for event in pygame.event.get():
            #prints all events within the window: print(event)
            #if pygame function QUIT is called (by clicking on the x):
            if event.type == pygame.QUIT:
                #set gameExit to true which exits the while loop
                gameExit = True
            
            #if arrowkey is pressed:
            if event.type == pygame.KEYDOWN:
                global sDirection
                if event.key == pygame.K_LEFT:
                    head_x_change = -block_size #left arrow down modify head variable -10 x position
                    head_y_change = 0
                    sDirection = "left"
                elif event.key == pygame.K_RIGHT:
                    head_x_change = block_size #right arrow down modify head variable +10 x position
                    head_y_change = 0
                    sDirection = "right"
                elif event.key == pygame.K_UP:
                    head_y_change = -block_size #up arrow key down modify head variable -10 y position
                    head_x_change = 0
                    sDirection = "up"
                elif event.key == pygame.K_DOWN:
                    head_y_change = block_size #down arrow key down modify head variable +10 y position
                    head_x_change = 0
                    sDirection = "down"
                elif event.key == pygame.K_p:
                    pause()
        
        #create the boundaries for the game:
        if head_x >= display_width or head_x < 0 or head_y > display_height or head_y < 0:
            gameOver = True
        #head apple collision detection:
        #basically if the entire head is outside the entire apple nothing will happen
        #once the head hits the apple it prints xy collision
        if head_x < randAppleX + appleThickness and head_x > randAppleX - block_size and head_y < randAppleY + appleThickness and head_y > randAppleY - block_size:
            #generate a new apple in a random location:
            #remember that randapplex and y are called within the game loop,
            #below; when drawing the apple it references these two variables
            randAppleX, randAppleY = randAppleGen()
            #after hitting an apple add 1 to the snakeLength
            snakeLength += 1
           

        #set the head x and y position to equal the modified amount of change
        #this will execute each iteration of the loop
        #and effectively moves the head continually until a different key direction 
        #is pressed.  
        head_x += head_x_change
        head_y += head_y_change

        #calls our gameDisplay variable and pygame's fill function
        #will fill the entire display lgrey
        gameDisplay.fill(lgrey)
        
        #draw the apple:
        #pygame.draw.rect(gameDisplay, maroon, [randAppleX, randAppleY, appleThickness, appleThickness])
        gameDisplay.blit(apple_image, (randAppleX, randAppleY))
        
        
        snakeHead = []
        #add the head x position to the snakehead list
        snakeHead.append(head_x)
        #add the head y position to the snakehead list
        snakeHead.append(head_y)
        #add the snakehead list to the snakelist
        snakeList.append(snakeHead)        
        
        #if the amount of elements (x and y positions of the head)
        #in snake list is > length of the snake:
        if len(snakeList) > snakeLength:
            #delete the first element
            # so with each iteration of the loop the first element is deleted
            # and another is appended
            # this way the snake is maintained at the value of the snakeLength variable
            del snakeList[0]
            #print(snakeList)

        #if snake runs into itself
        #for each segment from first up to the last in the list:
        for eachSegment in snakeList[0:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        #draw snake:
        drawSnake(block_size, snakeList)
        
        #put the score up:
        score(snakeLength - 1)

        #updates the display with the current changes
        pygame.display.update()
        
        #define frames per second in the argument
        #forces the while loop to run 15 times per second
        #better to modify movement variables than fps because fps 
        #will drain processing power
        clock.tick(fps)

    
    #uninitialize all the modules
    pygame.quit()
    #quit python
    quit()



#Call the game intro:
gameIntro()
#Call the game loop:
gameLoop()