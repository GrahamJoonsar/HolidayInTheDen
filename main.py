import pygame
import math

# Window Setup
windowWidth = 500
windowHeight = 500
pygame.init()
win = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("SnowMan")
numOfPlayers = 8
bounciness = 3

def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# Snowman(Player) class
class Snowman:
    def __init__(self, snowManNumber):
        self.x = math.cos(2*math.pi/numOfPlayers*(snowManNumber+1)) * 200 + windowWidth/2
        self.y = math.sin(2*math.pi/numOfPlayers*(snowManNumber+1)) * 200 + windowHeight/2
        self.number = snowManNumber
        self.xVel = 0
        self.yVel = 0
        
    def collide(self, otherx, othery):
        angle = math.atan2(self.y - othery, self.x - otherx)
        self.xVel = math.cos(angle) * bounciness
        self.yVel = math.sin(angle) * bounciness
        

    def move(self):
        if 20 < self.x + self.xVel < windowWidth - 20:
            self.x += self.xVel
        else:
            self.xVel = 0

        if 20 < self.y + self.yVel < windowHeight - 20:
            self.y += self.yVel
        else:
            self.yVel = 0
            
    def draw(self):
        pygame.draw.circle(win, (255, 255, 255), (self.x, self.y), 20)
        

snowManList = []

for i in range(numOfPlayers):
    snowManList.append(Snowman(i))

# Main game Loop
running = True
while running:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    mousex, mousey = pygame.mouse.get_pos()

    snowManList[0].x = mousex
    snowManList[0].y = mousey

    win.fill((100, 100, 255))

    for snowman in snowManList:
        snowman.draw()
        snowman.move()
        for snowman2 in snowManList:
            if distance(snowman.x, snowman.y, snowman2.x, snowman2.y) <= 40 and snowman.number != snowman2.number:
                tempx = snowman.x
                tempy = snowman.y
                snowman.collide(snowman2.x, snowman2.y)
                snowman2.collide(tempx, tempy)

    pygame.display.update()

pygame.quit()
