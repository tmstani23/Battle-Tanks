import pygame
import time
import random

#this is a test of pygame

#initialize the pygame modules
#there are six so check init should return the initialized modules
#if pygame is correctly installed and initialized:
checkInit = pygame.init()
print(checkInit)

#define screen width and height variables:
display_width = 800
display_height = 600

#define color variables:
black = (25,25,25)
dgrey = (51,51,51)
blue = (66,139,202)
white = (230,230,230)
green = (128,240,119)
l_green = (169, 245, 163)
ld_grey = (77,77,77)
l_blue = (136, 181, 221)

#define variables for the tank size:
tankWidth = 40
tankHeight = 20
turretWidth = 5
wheelWidth = 5

#ground variables
ground_height = 35

#define font variables:
tinyFont = pygame.font.SysFont("comicsansms", 12)
smallFont = pygame.font.SysFont("comicsansms", 25)
medFont = pygame.font.SysFont("comicsansms", 50)
largeFont = pygame.font.SysFont("comicsansms", 80)

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


def explosion(hit_x, hit_y, size=50):
    #explode is the condition on which the while loop depends to continue looping
    explode = True
    #exitable while loop that finds a startpoint and explosions of random color and size at impact location
    #depending on magnitude
    while explode:
        for event in pygame.event.get():
            #if the user clicks the X at the top right, quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #startpoint takes in hit_x,y variables from outside the function
        startPoint = hit_x, hit_y
        #colorchoices for the explosions
        colorChoices = [blue, l_blue, green, l_green]
        #controls number of explosions
        magnitude = 1
        #while number of explosions is < 50:
        while magnitude < size:
            #starting at x begin a random range of numbers from -1 * magnitude value to magnitude value
            #this will cause the shell to start at the center x and expand outwards
            exploding_bit_x = hit_x + random.randrange(-1 * magnitude, magnitude)
            #same as above except at the y location
            exploding_bit_y = hit_y + random.randrange(-1 * magnitude, magnitude)
            #draw the explosion to the screen(where, random color from colorChoices list, (impact location x,y), random pixel radius between 1 and 5)
            pygame.draw.circle(gameDisplay, colorChoices[random.randrange(0,4)], (exploding_bit_x, exploding_bit_y), random.randrange(1,5))
            #add one to the magnitude value
            magnitude += 1
            #update the screen and tick the clock 100 times 
            pygame.display.update()
            clock.tick(100)
        #exit the while loop    
        explode = False

#create function that draws the shell to the screen
#(xy is the return from the tank function, and 
#   currentTurretPos is the position within listofPossibleTurrets
#       this list contains x,y coordinates for the x and y position of the turret)
def fireShell(xy, mainTankX, mainTankY, currentTurretPos, fire_power, barrierX, barrierY, barrier_width):
    fire = True
    #save xy into variable startingShell
        #and convert the results from xy into a list 
        #because they were in tuple format and couldn't be modified
    startingShell = list(xy)
    print("Fire!", xy)
    print(currentTurretPos)
    
    #begin looping while the condition fire is true:
    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print(startingShell[0], startingShell[1])
        #draw a green circle to the screen with a center at xy positions startingShell[0] and [1] and make it 5 pixels wide
        pygame.draw.circle(gameDisplay, green, (startingShell[0], startingShell[1]), 5)
        
        #if statement that controls whether friendly tank is going to fire a shell
        #start the beginning shell x position at startingShell[0] and move it left across the screen
        startingShell[0] -= (12 - currentTurretPos)*2 
        
        #add the below calculation to the startingShell[1] position each iteration of the loop
        #this controls the behavior of the shell's y trajectory
        #here the fire_power is added and divided by 50
        #this makes the shell fire stronger or weaker depending on the value of fire_power
        #a lower number is more power and a higher number is less
        startingShell[1] += int((((startingShell[0] -xy[0])*0.015/(fire_power/50))**2) - (currentTurretPos + currentTurretPos / (12 - currentTurretPos)))
        
        #determine if the shell hit the ground then run the code:
        if startingShell[1] > display_height - ground_height:
            #print x and y location of the last shell on the to leave the screen
            print("Last shell:", startingShell[0], startingShell[1])
            #create to variables that holds
            #algorithm that uses cross multiplication to determine where 
            #shell hits on the screen and then print location
            hit_x = int((startingShell[0]*display_height-ground_height)/startingShell[1])
            hit_y = int(display_height-ground_height)
            print("Impact:", hit_x, hit_y)
            #call function that creates an explosion at impact location
            explosion(hit_x, hit_y)
            #fire is false so the while loop ends
            fire = False
        
        #create variables that check all sides of the barrier for barrier shell collisions
        #check_x_1 determines x position of shell is less than the barrier verticle side and not within the barrier width
        check_x_1 = startingShell[0] <= barrierX + barrier_width
        #check_x_2 determines x position of shell is greater than the barrier verticle sides
        check_x_2 = startingShell[0] >= barrierX
        #check_y_1 and check_y_2 determines y position of shell is less than the display height 
            #but greater than the top horizontal side of the barrier
        check_y_1 = startingShell[1] <= display_height
        check_y_2 = startingShell[1] >= display_height - barrierY

        #if all the above check conditions are true run the code:
        if check_x_1 and check_x_2 and check_y_1 and check_y_2:

            #print x and y location of the last shell on the to leave the screen
            print("Last shell:", startingShell[0], startingShell[1])
            #create to variables that holds
            #the value of the shells current x and y location
            hit_x = int(startingShell[0])
            hit_y = int(startingShell[1])
            print("Impact:", hit_x, hit_y)
            #call function that creates an explosion at impact location
            explosion(hit_x, hit_y)
            #fire is false so the while loop ends
            fire = False    
            
        pygame.display.update()
        clock.tick(30)

#create enemy fire shell function.  Same as regular fireshell with minor changes:
def eFireShell(xy, mainTankX, mainTankY, currentTurretPos, fire_power, barrierX, barrierY, barrier_width):
    fire = True
    startingShell = list(xy)
    print("Fire!", xy)
    print(currentTurretPos)
    
    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print(startingShell[0], startingShell[1])
        pygame.draw.circle(gameDisplay, green, (startingShell[0], startingShell[1]), 5)
        
        #if statement that controls whether enemy tank is going to fire a shell
        #start the beginning shell x position at startingShell[0] and move it right across the screen
        startingShell[0] += (12 - currentTurretPos)*2 
        #main shell arc algorithm:
        startingShell[1] += int((((startingShell[0] -xy[0])*0.015/(fire_power/50))**2) - (currentTurretPos + currentTurretPos / (12 - currentTurretPos)))
        
        #determine if the shell hit the ground then run the code:
        if startingShell[1] > display_height - ground_height:
            print("Last shell:", startingShell[0], startingShell[1])
            hit_x = int((startingShell[0]*display_height-ground_height)/startingShell[1])
            hit_y = int(display_height-ground_height)
            print("Impact:", hit_x, hit_y)
            explosion(hit_x, hit_y)
            fire = False
        
        check_x_1 = startingShell[0] <= barrierX + barrier_width
        check_x_2 = startingShell[0] >= barrierX
        check_y_1 = startingShell[1] <= display_height
        check_y_2 = startingShell[1] >= display_height - barrierY

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            print("Last shell:", startingShell[0], startingShell[1])
            hit_x = int(startingShell[0])
            hit_y = int(startingShell[1])
            print("Impact:", hit_x, hit_y)
            explosion(hit_x, hit_y)
            fire = False    
            
        pygame.display.update()
        clock.tick(30)


#define the enemy tank function that draws the tank elements:
#arguments x, y for where the tank will be placed
#mainTankX and mainTankY are filled in for x and y here when enemy_tank() is called in the gameLoop
def enemy_tank(x, y, turretPos):
    #convert the x,y to integers because they will be passed
        #into the function as floats from mainTankX and mainTankY
        #and it is necessary they remain whole numbers
    x = int(x)
    y = int(y)

    #positions for x and y points of the turret
    #effectively changes line angle of turret
    possibleTurrets = [(x+27, y-2),
                                (x+26, y-5),
                                (x+25, y-8), 
                                (x+23, y-12),
                                (x+20, y-14),
                                (x+18, y-15),
                                (x+15, y-17),
                                (x+13, y-19),
                                (x+11, y-21)
                                ]
    
    #draw circle for the tank turret:
    pygame.draw.circle(gameDisplay, black, (x, y), int(tankHeight/2))
    #draw tank body:
    pygame.draw.rect(gameDisplay, black, (x-tankHeight, y, tankWidth, tankHeight))
    #draw the gun (where, color, turret x,y,  end point locations, width of line)
    #when the tank() function is called the index position is passed in and the  possible turret
        #position at that inded position will be selected.
    #This is important because it is responsible for drawing the turret at different angles
    pygame.draw.line(gameDisplay, black, (x,y), possibleTurrets[turretPos], turretWidth)
    
    
    #create variable for starting x position to be used to align first wheel
    startX = int(tankWidth/2) #here it is 5
    #Draw 9 wheels next to each other using for loop
    for i in range(9):
        #draw one circle for each iteration  of the loop
        pygame.draw.circle(gameDisplay, black, (x-startX, y+tankHeight), wheelWidth)
        #subtract 5 from startX each iteration of the loop
        startX -= 5
    #returns the current x,y positions of the turret from the possibleTurrets list
    #this is used later in the gun function to know where the turret is shooting from
    return possibleTurrets[turretPos]

def tank(x, y, turretPos):
    #essentially the same as enemy tank so comments will only relinquish changes
    x = int(x)
    y = int(y)
    possibleTurrets = [(x-27, y-2),
                                (x-26, y-5),
                                (x-25, y-8), 
                                (x-23, y-12),
                                (x-20, y-14),
                                (x-18, y-15),
                                (x-15, y-17),
                                (x-13, y-19),
                                (x-11, y-21)
                                ]
    
    pygame.draw.circle(gameDisplay, black, (x, y), int(tankHeight/2))
    pygame.draw.rect(gameDisplay, black, (x-tankHeight, y, tankWidth, tankHeight))
    pygame.draw.line(gameDisplay, black, (x,y), possibleTurrets[turretPos], turretWidth)
   
    startX = int(tankWidth/2) 
   
    for i in range(9):
        pygame.draw.circle(gameDisplay, black, (x-startX, y+tankHeight), wheelWidth)
        startX -= 5
    return possibleTurrets[turretPos]


#define text to button function (text, color, (x,y,width,height)):
def text_to_button(msg, color, buttonX, buttonY, buttonWidth, buttonHeight, size = "small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (buttonX + (buttonWidth / 2)), buttonY + (buttonHeight / 2)
    #display the two text objects to the screen:
    gameDisplay.blit(textSurf, textRect)

def game_controls():
    
    gameControls = True
    #while loop that controls events that happen in the game intro screen
    while gameControls:
        #for any event that happens get the event from pygame library
        for event in pygame.event.get():
            #if user clicks the X to close the game:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
        #fill the screen with a white background
        gameDisplay.fill(white)
        
        #create messages to screen showing what the controls are
        #the third argument is y axis variance
        message_to_screen("Controls", blue, -160, "medium")
        message_to_screen("Fire: spacebar", dgrey, -80, "small")
        message_to_screen("Move turret: up and down arrows", dgrey, -40, "small")
        message_to_screen("Move tank: left and right arrows", dgrey, 0, "small")
        message_to_screen('Pause: press "p"', dgrey, 40, "small")

        #define a variable that holds the current mouse position x,y as a tuple
        mCursor = pygame.mouse.get_pos()
        
        #call text_to_button function to draw text onto the buttons:
        button("Play", 150, 400, 100, 50, dgrey, ld_grey, action = "Play")
        button("Menu", 350, 400, 100, 50, green, l_green, action = "Menu")
        button("Quit", 550, 400, 100, 50, blue, l_blue, action = "Quit")

        #update and iterate clock tick at 15 fps
        pygame.display.update()
        clock.tick(fps)


#define button function
def button (text, x, y, width, height, inactive_color, active_color, action = None):
    #gets the mouse position as a tuple of x,y values 
    mCursor = pygame.mouse.get_pos()
    #gets when the mouse button is pressed as a tuple where [0] is not pressed and [1] is pressed
    mClick = pygame.mouse.get_pressed()
    #basically if the mouse cursor is within the button x and y boundries:
    if x + width > mCursor[0] > x and y + height > mCursor[1] > y:
        #draw the button with active color:
        pygame.draw.rect(gameDisplay, active_color, (x, y, width, height))
        #if mouse clicks on the X at the top right then quit:
        if mClick[0] == 1 and action != None:
            if action == "Quit":
                pygame.quit()
                quit()
            #if mouse clicks on controls button go to controls menu
            if action == "Controls":
                game_controls()
            #go to game loop and play the game screen
            if action == "Play":
                gameLoop()
            #go to the menu screen when menu button is clicked
            if action == "Menu":
                gameIntro()
    else:
        #if mouse is not over any button display the button with inactive color
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, width, height))
    #draw the text onto the buttons
    text_to_button(text,black,x,y,width,height,)


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

#add a function to draw a barrier to separate the two tanks:
def barrier(barrierX, barrierY, barrier_width):
    
    #draw the barrier to screen 50 is the width barrierY is the height:
    pygame.draw.rect(gameDisplay, black, [barrierX, display_height - barrierY, barrier_width, barrierY])


#define the pause function
def pause():
    paused = True
    
    #display paused messages
    message_to_screen("Paused", blue, -100, size = "large")
    message_to_screen("Press 'C' to continue or 'Q' to quit", green, -20)
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
    text = smallFont.render("Score: " +str(score), True, dgrey)
    gameDisplay.blit(text, [0,0])

def power(fire_power):
    text = smallFont.render("Power: " +str(fire_power) + "%", True, black)
    gameDisplay.blit(text, [display_width/2, 0])

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
        #fill the screen with a white background
        gameDisplay.fill(white)
        message_to_screen("Welcome to Battle Tanks!", blue, -160, "medium")
        message_to_screen("The objective of the game is to shoot and destroy", dgrey, -80, "small")
        message_to_screen("the enemy tanks before they destroy you.", dgrey, -40, "small")
        message_to_screen("The more enemies you kill the harder they get.", dgrey, 0, "small")
       # message_to_screen("Press 'C' to play, 'P' to pause, or 'Q' to quit.", green, 60, "small")
        message_to_screen("Created by Timothy Stanislav; Indoorkin Productions", dgrey, 225, "tiny")

        #define a variable that holds the current mouse position x,y as a tuple
        mCursor = pygame.mouse.get_pos()
        
        #call text_to_button function to draw text onto the buttons:
        button("Play", 150, 400, 100, 50, dgrey, ld_grey, action = "Play")
        button("Controls", 350, 400, 100, 50, green, l_green, action = "Controls")
        button("Quit", 550, 400, 100, 50, blue, l_blue, action = "Quit")

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

    #define variables for the friendly tank positions:
    mainTankX = display_width * 0.9
    mainTankY = display_height * 0.9
    tankMove = 0

    #define enemy tank variables:
    enemyTankX = display_width * 0.1
    enemyTankY = display_height * 0.9
    
    #variables for the power of the shot and the change in power:
    fire_power = 50
    power_change = 0

    #define variables for the turret position and turret position change:
    currentTurretPos = 0
    changeTurretPos = 0

    #create main barrier variables:
    #generate barrier starting from the middle and randomly between + or - 20 percent of the display width
    barrierX = (display_width / 2) + random.randint(-.2*display_width, .2*display_width)
    barrierY = random.randrange(display_height*.1, .6*display_height)
    barrier_width = 50

   
    while not gameExit:
        
        if gameOver == True:
           #display 2 messages 
            message_to_screen("You lose!", blue, y_displace = -160, size = "large")
            message_to_screen("Press 'C' to play again or 'Q' to Quit.", 
            green, y_displace = -80, size = "small") 
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
    
                #move tank left or right and turret up or down when keys are pressed
                if event.key == pygame.K_LEFT:
                    tankMove = -5
                elif event.key == pygame.K_RIGHT:
                    tankMove = 5
                elif event.key == pygame.K_UP:
                    changeTurretPos = 1
                elif event.key == pygame.K_DOWN:
                    changeTurretPos = -1
                elif event.key == pygame.K_p:
                    pause()
                #if spacebar is pressed execute fire shell function
                elif event.key == pygame.K_SPACE:
                    #gun is the variable that holds the tank function
                    #This draws the tank entire tank to the screen
                    #and returns the current position of the turret
                    fireShell(gun, mainTankX, mainTankY, currentTurretPos, fire_power,barrierX, barrierY, barrier_width)
                    eFireShell(enemy_gun, enemyTankX, enemyTankY, 8, 50,barrierX, barrierY, barrier_width)
                elif event.key == pygame.K_a:
                    power_change = -1
                elif event.key == pygame.K_d:
                    power_change = 1

            #if arrow key is released:
            elif event.type == pygame.KEYUP:
                #if the tank is already moving in a direction when key is released set speed to zero
                #this way one can press left first then right to start moving left then right 
                    #without messing up the movement or stopping in place.
                #Also allows stopping when all keys are released.
                if event.key == pygame.K_LEFT and tankMove == -5:
                    tankMove = 0
                elif event.key == pygame.K_RIGHT and tankMove == 5:
                    tankMove = 0
                #similarly, if up or down is released stop changing the turret position
                    #so the turret stops moving
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    changeTurretPos = 0
                #once the a or d key is released power_change resets to zero 
                    #so the change doesn't keep going infinitely adding or subtracting power
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    power_change = 0
        
        
        #set variable mainTankX equal to tank move so when tank is called
        #it moves the amount specified in tank move in the keypress event handling
        mainTankX += tankMove
        
        #set variable currentTurretPos equal to changeTurretPos so when tank is called
        #it moves the turret the amount specified in the keypress event handling
        currentTurretPos += changeTurretPos

        #if the current position exceeds 8 the game will crash
            #because there are only 8 turret positions in the possibleTurrets list
        #so this code restricts the positions to 8:
        if currentTurretPos > 8:
            currentTurretPos = 8
        elif currentTurretPos < 0:
            currentTurretPos = 0


        #logic for what happens when tank crashes into the barrier:
        if mainTankX - (tankWidth/2) < barrierX + barrier_width:
            mainTankX += 5
        
        
        #calls our gameDisplay variable and pygame's fill function
        #will fill the entire display white
        gameDisplay.fill(white)
        
        
        #call the tank function to draw the tank onto the screen:
        #note: the call is after the above fill otherwise the tank
            #would be drawn over by the background
        gun = tank(mainTankX, mainTankY, currentTurretPos)

        #call the function to draw the enemy tank:
        #8 is the eight position in the possibleTurrets list
        #this means the enemy gun won't move it will remain in last position.
        enemy_gun = enemy_tank(enemyTankX, enemyTankY, 8) 
        
        #firepower = firepower + power_change
        fire_power += power_change
        #call the function firepower which displays the power to the screen
        power(fire_power)

        #draw the barrier to the screen:
        barrier(barrierX, barrierY, barrier_width)
        #draw ground to the screen(color, shape[starting x, starting y, width, height])
        gameDisplay.fill(green, rect = [0, display_height-ground_height, display_width, ground_height])

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