import pygame
import time
import random



#initialize the pygame modules
#there are six so check init should return the initialized modules
#if pygame is correctly installed and initialized:
checkInit = pygame.init()
print(checkInit)
#print(pygame.font.get_fonts())

#define screen width and height variables:
display_width = 800
display_height = 600

#create the game surface with resolution of 800 x 600:
gameDisplay = pygame.display.set_mode((display_width, display_height))

#define color variables:
black = (25, 25, 25)
dgrey = (51, 51, 51)
blue = (66, 139, 202)
lgrey = (139, 174, 186)
green = (128, 240, 119)
l_green = (169, 245, 163)
ld_grey = (77, 77, 77)
l_blue = (136, 181, 221)
yellow = (255, 255, 0)
red = (255, 0, 0)

#sound file variables
fireSound = pygame.mixer.Sound("c:/Tim's Files/my dream/learning/Programming/python/Tanks/explosion4.wav")
explosionSound = pygame.mixer.Sound("c:/Tim's Files/my dream/learning/Programming/python/Tanks/explosion1.wav")

#define variables for the tank size:
tankWidth = 40
tankHeight = 20
turretWidth = 2
enemyTurretWidth = 2
wheelWidth = 5

#image file variables:
playerTankImage = pygame.image.load("c:/Tim's Files/my dream/learning/Programming/python/Tanks/tank1real.png")
enemyTankImage = pygame.image.load("c:/Tim's Files/my dream/learning/Programming/python/Tanks/tank2real.png")
#background image
bgImage = pygame.image.load("c:/Tim's Files/my dream/learning/Programming/python/Tanks/nightsky.jpg").convert()


#ground variables
ground_height = 35

#define font variables:
tinyFont = pygame.font.SysFont('caslon', 15)
smallFont = pygame.font.SysFont("caslon", 25)
medFont = pygame.font.SysFont("centurygothic", 75)
largeFont = pygame.font.SysFont("centurygothic", 100)

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
fps = 20

#create screen message function:
def message_to_screen(msg, color, y_displace = 0, size = "small"):
    #create two variables that are now each text_objects functions:
    textSurf, textRect = text_objects(msg, color, size)
    #set textRect.center to = the center of the display:
    textRect.center = (display_width / 2), (display_height / 2 + y_displace)
    #display the two text objects to the screen:
    gameDisplay.blit(textSurf, textRect)


def explosion(hit_x, hit_y, size=50):
    #play sound for the explosion
    pygame.mixer.Sound.play(explosionSound)
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
        colorChoices = [blue, l_blue, green, l_green, ld_grey, dgrey]
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
            pygame.draw.circle(gameDisplay, colorChoices[random.randrange(0,6)], (exploding_bit_x, exploding_bit_y), random.randrange(1,5))
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
def fireShell(xy, mainTankX, mainTankY, currentTurretPos, fire_power, barrierX, barrierY, barrier_width, enemyTankX, enemyTankY):
    #play sound for shell firing
    pygame.mixer.Sound.play(fireSound)
    fire = True
    damage = 0
    #save xy into variable startingShell
        #and convert the results from xy into a list 
        #because they were in tuple format and couldn't be modified
    startingShell = list(xy)
    
    #begin looping while the condition fire is true:
    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #draw a green circle to the screen with a center at xy positions startingShell[0] and [1] and make it 5 pixels wide
        pygame.draw.circle(gameDisplay, l_green, (int(startingShell[0]), startingShell[1]), 3)
        
        #if statement that controls whether friendly tank is going to fire a shell
        #start the beginning shell x position at startingShell[0] and move it left across the screen
        startingShell[0] -= (12 - currentTurretPos)*0.9 
        
        #add the below calculation to the startingShell[1] position each iteration of the loop
        #this controls the behavior of the shell's y trajectory
        #here the fire_power is added and divided by 50
        #this makes the shell fire stronger or weaker depending on the value of fire_power
        #a lower number is more power and a higher number is less
        startingShell[1] += int((((startingShell[0] -xy[0])*0.015/(fire_power/50))**2) - (currentTurretPos + currentTurretPos / (12 - currentTurretPos)))
        
        #determine if the shell hit the ground then run the code:
        if startingShell[1] > display_height - ground_height:
            #create to variables that holds
            #algorithm that uses cross multiplication to determine where 
            #shell hits on the screen and then print location
            hit_x = int((startingShell[0]*display_height-ground_height)/startingShell[1])
            hit_y = int(display_height-ground_height)
             
            
            #find center of enemy tank and modify damage variable
            #to register the hit
            #Assigns different damage amounts based on how close the shot is to the tank x center
            if enemyTankX + 10 > hit_x > enemyTankX - 10:
                print("Critical Hit!")
                damage = 35
            elif enemyTankX + 15 > hit_x > enemyTankX - 15:
                print("Hard Hit!")
                damage = 25
            elif enemyTankX + 25 > hit_x > enemyTankX - 25:
                print("Medium Hit!")
                damage = 15
            elif enemyTankX + 35 > hit_x > enemyTankX - 35:
                print("Light Hit!")
                damage = 5
            
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
        clock.tick(50)
    return damage

#create enemy fire shell function.  Same as regular fireshell with minor changes:
def eFireShell(xy, enemyTankX, enemyTankY, currentTurretPos, fire_power, barrierX, barrierY, barrier_width, mainTankX, mainTankY):
    #play shell firing sound:
    pygame.mixer.Sound.play(fireSound)
    #damage is veriable that holds amount of damage from a hit
    damage = 0
    #currentPower is the current power of the enemy tank
    #one is added each iteration to test all possible powers and hone in on the currect power to hit the player tank
    currentPower = 1
    powerFound = False
    #this loop takes many invisible shots until it finds the player tank X location
    #then it acquires that location and exits the loop
    #begin looping while powerFound = False:
    while not powerFound:
        #add 1 to currentPower each iteration of the loop
        currentPower += 1
        #after 100 different tries powerFound = True and the loop exits
        if currentPower > 100:
            powerFound = True
        
        #define variables for the next loop which fires the shot 
        fire = True
        #converts xy into a list.  xy is the return from the tank function which is possible turrets xy positions
        startingShell = list(xy)
        
        while fire:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                       
            #if statement that controls whether enemy tank is going to fire a shell
            #start the beginning shell x position at startingShell[0] and move it right across the screen
            startingShell[0] += (12 - currentTurretPos)*0.9 
            #main shell Y arc algorithm:
            startingShell[1] += int((((startingShell[0] -xy[0])*0.015/(currentPower/50))**2) - (currentTurretPos + currentTurretPos / (12 - currentTurretPos)))
            
            
            #determine if the shell hit the ground then run the code:
            if startingShell[1] > display_height - ground_height:
                hit_x = int((startingShell[0]*display_height-ground_height)/startingShell[1])
                hit_y = int(display_height-ground_height)
                #if the shot was between maintankX + 15 set powerFound to true and exit the loop
                #this way the currentPower setting is now fixed at the player tank location
                if mainTankX + 15 > hit_x > mainTankX:
                    print("Target Acquired")
                    powerFound = True
                
                fire = False
            
            check_x_1 = startingShell[0] <= barrierX + barrier_width
            check_x_2 = startingShell[0] >= barrierX
            check_y_1 = startingShell[1] <= display_height
            check_y_2 = startingShell[1] >= display_height - barrierY

            if check_x_1 and check_x_2 and check_y_1 and check_y_2:
                hit_x = int(startingShell[0])
                hit_y = int(startingShell[1])
                fire = False    
        
    #repeat the fire loop again this time actually drawing the shell and explosion to the screen    
    fire = True
    startingShell = list(xy)
    #variable that adds randomness to the enemy current power:
    randomPower = random.randrange(int(currentPower*0.9), int(currentPower*1.00))

    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        #here the shell is drawn
        pygame.draw.circle(gameDisplay, l_blue, (int(startingShell[0]), startingShell[1]), 3)
        
        

        startingShell[0] += (12 - currentTurretPos)*0.9
        startingShell[1] += int((((startingShell[0] -xy[0])*0.015/(randomPower/50))**2) - (currentTurretPos + currentTurretPos / (12 - currentTurretPos)))
        
        if startingShell[1] > display_height - ground_height:
            print("Last shell:", startingShell[0], startingShell[1])
            hit_x = int((startingShell[0]*display_height-ground_height)/startingShell[1])
            hit_y = int(display_height-ground_height)
            print("Impact:", hit_x, hit_y)
            
            #find center of player tank and modify damage variable
            #to register the hit change damage to 25
            if mainTankX + 10 > hit_x > mainTankX - 10:
                print("Critical Hit!")
                damage = 25
            elif mainTankX + 15 > hit_x > mainTankX - 15:
                print("Hard Hit!")
                damage = 18
            elif mainTankX + 25 > hit_x > mainTankX - 25:
                print("Medium Hit!")
                damage = 10
            elif mainTankX + 35 > hit_x > mainTankX - 35:
                print("Light Hit!")
                damage = 5

            #call the explosion
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
            #below the explosion is called
            explosion(hit_x, hit_y)
            fire = False    
            
        pygame.display.update()
        clock.tick(50)
    #return the current value of damage variable when called
    return damage


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
    possibleTurrets = [(x+27, y-4),
                                (x+26, y-5),
                                (x+25, y-8), 
                                (x+23, y-12),
                                (x+20, y-14),
                                (x+18, y-15),
                                (x+15, y-17),
                                (x+13, y-19),
                                (x+11, y-21)
                                ]
                                
    #display the tank1 image at maintank element locations:
    gameDisplay.blit(enemyTankImage, (x-tankHeight, y+4))

    #draw circle for the tank turret:
    #pygame.draw.circle(gameDisplay, black, (x, y), int(tankHeight/2))
    #draw tank body:
    #pygame.draw.rect(gameDisplay, black, (x-tankHeight, y, tankWidth, tankHeight))
    #draw the gun (where, color, turret x,y,  end point locations, width of line)
    #when the tank() function is called the index position is passed in and the  possible turret
        #position at that inded position will be selected.
    #This is important because it is responsible for drawing the turret at different angles
    pygame.draw.line(gameDisplay, lgrey, (x-6,y+12), possibleTurrets[turretPos], enemyTurretWidth)
    
    
    #create variable for starting x position to be used to align first wheel
    startX = int(tankWidth/2) #here it is 5
    
    #Wheel code from previous version:
    
    #Draw 9 wheels next to each other using for loop
    #for i in range(9):
        #draw one circle for each iteration  of the loop
        #pygame.draw.circle(gameDisplay, black, (x-startX, y+tankHeight), wheelWidth)
        #subtract 5 from startX each iteration of the loop
        #startX -= 5
    #returns the current x,y positions of the turret from the possibleTurrets list
    #this is used later in the gun function to know where the turret is shooting from
    return possibleTurrets[turretPos]

def tank(x, y, turretPos):
    #essentially the same as enemy tank so comments will only relinquish changes
    x = int(x)
    y = int(y)
    possibleTurrets = [(x-27, y-4),
                                (x-26, y-5),
                                (x-25, y-8), 
                                (x-23, y-12),
                                (x-20, y-14),
                                (x-18, y-15),
                                (x-15, y-17),
                                (x-13, y-19),
                                (x-11, y-21)
                                ]
    
    #display the tank1 image at maintank element locations:
    gameDisplay.blit(playerTankImage, (x-tankHeight, y+4))
    #pygame.draw.circle(gameDisplay, black, (x, y), int(tankHeight/2))
    #pygame.draw.rect(gameDisplay, black, (x-tankHeight, y, tankWidth, tankHeight))
    pygame.draw.line(gameDisplay, ld_grey, (x+2,y+5), possibleTurrets[turretPos], turretWidth)
    
   
    # Wheel code from previous version:
    # startX = int(tankWidth/2) 
   
    #for i in range(9):
        #pygame.draw.circle(gameDisplay, black, (x-startX, y+tankHeight), wheelWidth-2)
        #startX -= 5
    
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
        gameDisplay.fill(dgrey)
        #define a variable that holds the current mouse position x,y as a tuple
        mCursor = pygame.mouse.get_pos()
        
        #create messages to screen showing what the controls are
        #the third argument is y axis variance
        message_to_screen("Controls", blue, display_height/2 -440, "medium")
        message_to_screen("Fire: 'Spacebar'", black, display_height/2 -340, "small")
        message_to_screen("Move turret: 'Up and down arrows'", black, display_height/2 -300, "small")
        message_to_screen("Move tank: 'Left and right arrows'", black, display_height/2 -260, "small")
        message_to_screen("Increase/decrease power: 'a/d'", black, display_height/2 -220, "small")
        message_to_screen("Pause: 'p'", black, display_height/2 -180, "small")

        #call text_to_button function to draw text onto the buttons:
        button("Play", display_width * 0.3 - 150, 475, 150, 50, black, ld_grey, action = "Play")
        button("Menu", display_width * 0.6 - 150, 475, 150, 50, black, l_green, action = "Menu")
        button("Quit", display_width * 0.9 - 150, 475, 150, 50, black, l_blue, action = "Quit")
       
        #update and iterate clock tick at 15 fps
        pygame.display.update()
        clock.tick(35)


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
        if mClick[0] == 1: 
            if action == "Quit":
                pygame.quit()
                quit()
            #if mouse clicks on controls button go to controls menu
            if action == "Controls":
                game_controls()
                intro = False
            #go to game loop and play the game screen
            if action == "Play":
                gameLoop()
            #go to the menu screen when menu button is clicked
            if action == "Menu":
                gameIntro()
                gameControls = False
    else:
        #if mouse is not over any button display the button with inactive color
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, width, height))
    #draw the text onto the buttons
    text_to_button(text,lgrey,x,y,width,height,)
   
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
    pygame.draw.rect(gameDisplay, lgrey, [barrierX, display_height - barrierY, barrier_width, barrierY])


#define the pause function
def pause():
    paused = True
    
    #display paused messages
    message_to_screen("Paused", blue, -100, size = "large")
    message_to_screen("Press 'c' to continue, 'm' for menu or 'q' to quit", l_green, -20)
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
                elif event.key == pygame.K_m:
                    gameIntro()
                #else if the q key: quit the game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
      
        #run 5 iterations of the loop
        clock.tick(15)

#define the score function:            
def score(score):
    #text variable uses smallFont function renders it with the message 
    #plus the string version of the score argument input
    text = smallFont.render("Score: " +str(score), True, dgrey)
    gameDisplay.blit(text, [0,0])


#function that displays text showing the power of the shot as a percent to the screen
def power(fire_power):
    text = smallFont.render("Power: " +str(fire_power) + "%", True, lgrey)
    gameDisplay.blit(text, [display_width/2 - display_width/12  , 0])

#function for the enemy and player health bars
def healthBars(playerHealth, enemyHealth):
    #if statements that modify healthcolor variables once health drops to certain ranges
    if playerHealth > 75:
        playerHealthColor = green
    elif playerHealth > 50:
        playerHealthColor = yellow
    else:
        playerHealthColor = red
    
    if enemyHealth > 75:
        enemyHealthColor = green
    elif enemyHealth > 50:
        enemyHealthColor = yellow
    else:
        enemyHealthColor = red
    #draw the two health bars to the screen as rectangles
    #player healthcolor changes as the variables are modified on shell hit
    pygame.draw.rect(gameDisplay, playerHealthColor, (680, 25, playerHealth, 25))
    pygame.draw.rect(gameDisplay, enemyHealthColor, (20, 25, enemyHealth, 25))

#define game intro screen function:
def gameIntro():
    intro = True
    #define a variable that holds the current mouse position x,y as a tuple
    mCursor = pygame.mouse.get_pos()
    
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
        gameDisplay.fill(dgrey)
        message_to_screen("Battle Tanks", blue, display_height/2 - 440, "large")
        message_to_screen("The objective of the game is to shoot and destroy", black,  display_height/2  - 340, "small")
        message_to_screen("the enemy tanks before they destroy you.", black, display_height/2 -300, "small")
        message_to_screen("The more enemies you kill the harder they get.", black, display_height/2 -260, "small")
       # message_to_screen("Press 'C' to play, 'P' to pause, or 'Q' to quit.", green, 60, "small")
        message_to_screen("Created by Timothy Stanislav: Indoorkin Productions", black, display_height/2 - 100, "tiny")
        
        #call text_to_button function to draw text onto the buttons:
        button("Play", display_width * 0.3 - 150, 400, 150, 50, black, ld_grey, action = "Play")
        button("Controls", display_width * 0.6 - 150, 400, 150, 50, black, l_green, action = "Controls")
        button("Quit", display_width * 0.9 - 150, 400, 150, 50, black, l_blue, action = "Quit")

        #update and iterate clock tick 30 times
        pygame.display.update()
        clock.tick(35)

        
#Create the primary game loop
#This loop runs while the game is being played
#It creates the background, the screen objects and 
#iterates the code over and over like a flip book animation
#function that controls what happens while gameover screen is active:
def gameOverScreen():
    game_over_screen = True
    #while loop that controls events that happen while the game is over:
    while game_over_screen:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
           
        gameDisplay.fill(dgrey)
        message_to_screen("Game Over!", blue, display_height/2 -440, "medium")
        message_to_screen("You have been destroyed.", black, display_height/2 -340, "small")

        #define a variable that holds the current mouse position x,y as a tuple
        mCursor = pygame.mouse.get_pos()
        
        button("Play Again", display_width * 0.3 - 150, 400, 150, 50, black, ld_grey, action = "Play")
        button("Controls", display_width * 0.6 - 150, 400, 150, 50, black, l_green, action = "Controls")
        button("Quit", display_width * 0.9 - 150, 400, 150, 50, black, l_blue, action = "Quit")

        pygame.display.update()
        clock.tick(30)

#Define win screen function
def winScreen():
    win_screen = True
    
    #while win screen is active:
    while win_screen:
       
        for event in pygame.event.get():
            #if user clicks the X to close the game:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
           
        gameDisplay.fill(dgrey)
        message_to_screen("You Win!", blue, display_height/2 - 400, "large")
        message_to_screen("Your enemy is vanquished.", black, display_height/2 - 300, "small")

        #define a variable that holds the current mouse position x,y as a tuple
        mCursor = pygame.mouse.get_pos()
        
        button("Play Again", display_width * 0.3 - 150, 400, 150, 50, black, ld_grey, action = "Play")
        button("Controls", display_width * 0.6 - 150, 400, 150, 50, black, l_green, action = "Controls")
        button("Quit", display_width * 0.9 - 150, 400, 150, 50, black, l_blue, action = "Quit")

        pygame.display.update()
        clock.tick(30)

        
#Create the primary game loop
#This loop runs while the game is being played
#It creates the background, the screen objects and 
#iterates the code over and over like a flip book animation
def gameLoop():
    gameExit = False
    gameOver = False

    #variables for player and enemy health:
    playerHealth = 100
    enemyHealth = 100
    
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
    barrierX = (display_width / 2) + random.randint(-.1*display_width, .1*display_width)
    barrierY = random.randrange(display_height*.1, .5*display_height)
    barrier_width = 10

    while not gameExit:
        
        if gameOver == True:
           #display 2 messages 
            message_to_screen("You lose!", blue, y_displace = -160, size = "large")
            message_to_screen("Press 'C' to play again or 'Q' to Quit.", 
            black, y_displace = -80, size = "small") 
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
                    #here damage calls fireshell then returns damage and sets it = to damage
                    damage = fireShell(gun, mainTankX, mainTankY, currentTurretPos, fire_power,barrierX, barrierY, barrier_width, enemyTankX, enemyTankY)
                    #subtract damage from enemy health
                    enemyHealth -= damage
                    #enemy_gun is the same for the enemy tank,
                    #8 is the enemy current turret position, from the possibleTurret list, and 50 is the starting fire power
                    #here damage calls eFireshell then returns damage and sets it = to damage
                    
                    #enemy tank movement variables:
                    ePossibleMovement = ["f", "r"]
                    #emoveIndex will always be 0,1 or 2 in this case f, neutral,reverse
                    eMoveIndex = random.randrange(0,2)
                    #randrange will cycle through the positions in the possibleMovement list
                    #for x in range from 0 to 10
                    for x in range(random.randrange(0,10)):
                        #if enemytankX position is between 30 percent of the display width and > 3 percent of the display width
                        if display_width * 0.5 > enemyTankX > display_width * 0.03:
                            
                            if enemyTankX + tankWidth >= barrierX:
                                print("enemy hit barrier, reversing...")
                                enemyTankX -= 10
                                
                            #if ePossibleMovement is position 1    
                            elif ePossibleMovement[eMoveIndex] == "f":
                                #logic for what happens when enemy tank crashes into the barrier:
                                #move enemytank forward 5 pixels
                                enemyTankX += 10
                            
                            #if ePossibleMovement is position 2
                            elif ePossibleMovement[eMoveIndex] == "r":
                                enemyTankX -= 10
                            
                    
                        elif enemyTankX < display_width * 0.97:
                            print("enemy hit edge")
                            enemyTankX += 10

                        else:
                            if enemyTankX + tankWidth >= barrierX:
                                print("enemy hit barrier, reversing...")
                                enemyTankX -= 10
                            
                            else: 
                                print("unknown enemyTankX position")
                                enemyTank -= 10

                        #draw enemy tank, healthbars,barrier,ground,etc to the screen: this exact code is done below with comments
                        gameDisplay.fill(lgrey)
                        
                        gameDisplay.blit(bgImage, [0, 0])
                        healthBars(playerHealth, enemyHealth)
                        gun = tank(mainTankX, mainTankY, currentTurretPos)
                        enemy_gun = enemy_tank(enemyTankX, enemyTankY, 8) 
                        fire_power += power_change
                        barrier(barrierX, barrierY, barrier_width)
                        power(fire_power)
                        gameDisplay.fill(dgrey, rect = [0, display_height-ground_height, display_width, ground_height])
                        pygame.display.update()     
                        clock.tick(fps)

                    
                    damage = eFireShell(enemy_gun, enemyTankX, enemyTankY, 8, 50, barrierX, barrierY, barrier_width, mainTankX, mainTankY)
                    #subtract damage from playerHealth 
                    playerHealth -= damage
                
                #if key a is pressed reduce power by one
                elif event.key == pygame.K_a:
                    power_change = -1
                #if key d is pressed increase power by one
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
        
        
        #calls the gameDisplay variable and pygame's fill function
        #will fill the entire display white
        gameDisplay.fill(lgrey)
        gameDisplay.blit(bgImage, [0, 0])

        #call function that displays the dynamic healthbar rects to screen
        #bugnote:if you reverse the order of the arguments here the healthbars will show up opposite sides
        healthBars(playerHealth, enemyHealth)
        
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
        #restricts fire power meter to between 1 and 100
        if fire_power > 100:
            fire_power = 100
        elif fire_power < 1:
            fire_power = 1
        
        #call the function firepower which displays the power to the screen
        power(fire_power)

        #draw the barrier to the screen:
        barrier(barrierX, barrierY, barrier_width)
        #draw ground to the screen(color, shape[starting x, starting y, width, height])
        gameDisplay.fill(dgrey, rect = [0, display_height-ground_height, display_width, ground_height])

        #updates the display with the current changes
        pygame.display.update()
        
        #logic that dictates when the game over and you win screens are activated
        #once player or enemy health < 1
        if playerHealth < 1:
            gameOverScreen()
        elif enemyHealth < 1:
            winScreen()

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
