import pygame
import math
import random
import time


# Window Setup
windowWidth = 500
windowHeight = 500

BLACK = (0,0,0)
WHITE = (255,255,255)


pygame.init()
pygame.font.init()
pygame.joystick.init()
win = pygame.display.set_mode((windowWidth, windowHeight))
clock = pygame.time.Clock()
pygame.display.set_caption("Pygame window!")
if pygame.joystick.get_count() == 0 :
    print("No joystick connected.")
    joystick = False
else :
    print("Joystick detected.")
    gamepad = pygame.joystick.Joystick(0)
    joystick = True



start_game = False





# make a timer for the game
# make a title and a background image for the game

# This is where you add the image loads
penguin = pygame.image.load("rotatedPenguin.png").convert_alpha()
present = pygame.image.load("present.png").convert_alpha()
gamepad = pygame.image.load("gamepad.png").convert_alpha()
menu = pygame.image.load("menu.png").convert_alpha()
start_button = pygame.image.load("StartButton.png").convert_alpha()
credits_button = pygame.image.load("CreditsButton.png").convert_alpha()
how_to_play_button = pygame.image.load("HowToPlay.png").convert_alpha()
working_start = pygame.image.load("workingStart.png").convert_alpha()
working_credits = pygame.image.load("workingCredit.png").convert_alpha()
working_HTP = pygame.image.load("workingHowToPlay.png").convert_alpha()
working_menu = pygame.image.load("workingMenu.png").convert_alpha()
start_small = pygame.transform.scale(start_button,(160,50))
credits_small = pygame.transform.scale(credits_button,(160,50))
how_to_play_small = pygame.transform.scale(how_to_play_button,(160,50))
working_start_small = pygame.transform.scale(working_start,(160,50))
working_credits_small = pygame.transform.scale(working_credits,(160,50))
working_HTP_small = pygame.transform.scale(working_HTP,(160,50))
working_menu_small = pygame.transform.scale(working_menu,(160,50))
penguin_medium = pygame.transform.scale(penguin,(100,100))
menu_medium = pygame.transform.scale(menu,(160,50))
present_medium = pygame.transform.scale(present,(100,100))






    
#delete the circle
class Timer() :
    def __init__(self) :
        self.counter = 100
        self.count_down = False
        self.font = pygame.font.SysFont('Arial', 50,bold = pygame.font.Font.bold)
        self.text = self.font.render(str(self.counter),True,(0,128,0))
        self.text_rect = self.text.get_rect()
        self.start_time = time.time()
    def update(self) :
        if self.count_down :
            menu = False
            if time.time() - self.start_time >= 1 :
                self.counter -=1
                self.start_time = time.time()
                self.text = self.font.render(str(self.counter),True,(0,128,0))
                if self.counter == 0 :
                    self.counter = 100
                    menu = True
            
            
               
    def draw(self) :
        if self.count_down :
            win.blit(self.text,(0,0))
        



#make a penguin that glides across the screen
class Sprites:
    def __init__(self) :
        self.image = penguin_medium
        self.num = 0
        self.x,self.y = windowWidth,windowHeight - self.image.get_width() - 10
        self.x_vel,self.y_vel = 0,0
        self.deleted = False
        self.speed = .5
        self.width = 60
        self.height = 60
        self.color = BLACK
        self.on_ground = False
    def update(self) :
        x_dir = -.05
        self.x += self.speed * x_dir
        if self.x < 0 :
            self.num += 1
            if self.num % 2 == 0 :
               self.image = penguin_medium
            else :
               self.image = present_medium
            self.x = windowWidth

    def draw(self) :
        win.blit(self.image,(self.x,self.y))
#find out how to set the textbox to a darker red color to hilight over it
# whichever button is darker red and you click on the button then it goes to the game
class Textbox:
    def __init__(self,xPos,yPos,dark_image,light_image,index) :
        self.button_light = light_image
        self.button_dark =  dark_image
        self.button_light.fill((255,0,0),special_flags = pygame.BLEND_RGB_ADD)
        self.index = index
        self.x = xPos
        self.isActive = False 
        self.deleted = False
        self.brighten = 128
        self.middle_x = windowWidth/2  - (self.x + self.button_light.get_width()/2)/2
        self.y = yPos
        self.textbox = 0
        self.pos = [self.x,self.y]
    def draw(self) :
        #only one is lighter
        if menuIndex == self.index:
           self.isActive = True
           win.blit(self.button_dark,self.pos)
        else :
            #only one is darker
           
           win.blit(self.button_light,self.pos)
        if direction.change  :
            #this makes a button when the menu is on how to play
            self.x = 0
            self.y = 0
            win.blit(self.button_light,self.pos)
        if not menu :
           if controlsIndex == self.index :
                win.blit(self.button_dark,self.pos)
        

class Direction :
    def __init__(self) :
        self.x = windowWidth/2 - 240
        self.y = 30
        self.width = 480
        self.height = 440
        self.index = 1
        self.gamepad_image = gamepad
        self.back_image_dark = working_menu_small
        self.back_image_light = menu_medium
        self.change = False
        self.objective_font = pygame.font.Font.render(pygame.font.SysFont('Arial',25),"Collect the presents and jump over the icebergs",True,pygame.Color(255,255,255))
        self.controls_font = pygame.font.Font.render(pygame.font.SysFont('Arial',25), "Controls",True,pygame.Color(255,255,255))
        self.color = (255,0,0)
    def draw(self) :
        global game_objects,ui_lists
        how_to_play_objects = []
        num = 0
        if self.change :
           pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.height))
           win.blit(self.objective_font,(self.x + 10 ,self.y))
           win.blit(self.controls_font,((self.x+windowWidth) /2-50,self.y + 40))
           win.blit(self.gamepad_image,(self.x + 10, self.y + 80))
           menu = Textbox(self.x,(self.y + self.height) - 50,self.back_image_dark,self.back_image_light,self.index)
           menu.draw()
           
        
           
 
            
            
           


        
    
           








# you do not need parameters for this one
# make a class for the textbox to have directions








Snowflake = []
for snow in range(100) :
    y_mov = random.randint(0,50)
    x = random.randint(0,windowWidth)
    y = random.randint(0,windowHeight+y_mov)
    Snowflake.append([x,y])

ui_lists = []
game_objects = []
deleted_ui = []
deleted_objects = []
paused = False
menu = True
menuIndex = 0
controlsIndex = 0
sprites = Sprites()
direction = Direction()
timer = Timer()

start = Textbox(160,100,working_start_small,start_small,0)
ui_lists.append(start)
creditsS = Textbox(160,200,working_credits_small,credits_small,1)
ui_lists.append(creditsS)
how_to_play = Textbox(160,300,working_HTP_small,how_to_play_small,2)
ui_lists.append(how_to_play)

game_objects.append(sprites)


running = True

while running:


    for event in pygame.event.get():


        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP and not paused :
                if menu :
                    menuIndex -=1
                    if menuIndex <= 0 :
                      menuIndex = 0
                elif not menu and menuIndex == 2 :
                    controlsIndex -= 1
                    if controlsIndex <= 0 :
                        controlsIndex = 0

            elif event.key == pygame.K_DOWN and not paused:
                if menu :
                    menuIndex += 1
                    if menuIndex >= 2:
                        menuIndex = 2
                elif not menu and menuIndex == 2:
                     controlsIndex += 1
                     if controlsIndex >= 1:
                         controlsIndex = 1
            
            elif event.key == pygame.K_RETURN and menuIndex == 2 and menu :
                     direction.change = True
                     menu = False
            elif event.key == pygame.K_RETURN and menuIndex ==  0 and menu :
                     timer.count_down = True
                     menu = False
            elif event.key == pygame.K_RETURN and controlsIndex == direction.index :
                 direction.change = False
                 menu = True
       






                #this checks to see whether the color was dark red is associated with the textbox

        
            
                
        
    

    
    win.fill((173,216,230))
    for snow in Snowflake :
        snow[1] += 0.03
        pygame.draw.circle(win,WHITE,snow,7)

        if snow[1] >= windowHeight :
            snow[1] = random.randrange(-50,-5)
            snow[0] = random.randrange(windowWidth)
    
        


    if menu :
        for textbox in ui_lists:
            if isinstance(textbox,Textbox) :
               textbox.draw()
        for objects in game_objects:
            if isinstance(objects,Sprites) :
                objects.draw()
    direction.draw()
    timer.draw()
    
    

#if you click on the game then it will pause until you click the escape button and then you will be able to play it again

    
    
    if not paused:
        pygame.display.update()
    sprites.update()
    if timer.count_down :
       timer.update()
       if timer.counter == 0:
           timer.counter = 5
           timer.count_down = False
           menu = True


    
    pygame.display.flip()
pygame.quit()

