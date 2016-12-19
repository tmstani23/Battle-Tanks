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

#define snake's head image:
#sh_image = pygame.image.load("c:/Tim's Files/my dream/learning/Programming/python/Snake Game/snakehead1.png")
#define apple image:
#apple_image = pygame.image.load("c:/Tim's Files/my dream/learning/Programming/python/Snake Game/apple2.png")

#create the game surface with resolution of 800 x 600:
gameDisplay = pygame.display.set_mode((display_width, display_height))
#Set the game title on the top bar:
pygame.display.set_caption('Battle Tanks')

#incorporate game icon
icon = pygame.image.load("c:/Tim's Files/my dream/learning/Programming/python/Snake Game/gameicon.jpg")
pygame.display.set_icon(icon)
#define a clock variable that tracks time in the game loop
clock = pygame.time.Clock()
#head position variables:

#frames per second variable:
fps = 15



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
        message_to_screen("Welcome to Battle Tanks!", blue, -160, "medium")
        message_to_screen("The objective of the game is to shoot and destroy", bgrey, -80, "small")
        message_to_screen("the enemy tanks before they destroy you.", bgrey, -40, "small")
        message_to_screen("The more enemies you kill the harder they get.", bgrey, 0, "small")
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

                if event.key == pygame.K_LEFT:
                    pass
                elif event.key == pygame.K_RIGHT:
                    pass
                elif event.key == pygame.K_UP:
                    pass
                elif event.key == pygame.K_DOWN:
                    pass
                elif event.key == pygame.K_p:
                    pause()
        
       

        #calls our gameDisplay variable and pygame's fill function
        #will fill the entire display lgrey
        gameDisplay.fill(lgrey)
        
       
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